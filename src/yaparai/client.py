"""HTTP client for YaparAI Public API + Enterprise API."""

from __future__ import annotations

import asyncio
import logging
import random
import httpx

from yaparai.config import YAPARAI_API_KEY, YAPARAI_BASE_URL

logger = logging.getLogger("yaparai")

# Module-level client for connection reuse across tool calls
_shared_client: httpx.AsyncClient | None = None


def _get_headers(api_key: str) -> dict:
    return {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "User-Agent": "yaparai-mcp/0.3.1",
    }


class YaparAIClient:
    """Async HTTP wrapper around the YaparAI API.

    Covers Public API (/v1/public/*), AI providers (/v1/ai/*),
    templates (/v1/comfy-templates/*), chatbot (/v1/chatbot/*),
    and Enterprise API (/api/enterprise/*).

    Reuses a shared httpx.AsyncClient for connection pooling.
    """

    def __init__(
        self,
        api_key: str | None = None,
        base_url: str | None = None,
    ):
        self.api_key = api_key or YAPARAI_API_KEY
        self.base_url = (base_url or YAPARAI_BASE_URL).rstrip("/")

        if not self.api_key:
            raise ValueError(
                "YAPARAI_API_KEY is not set. "
                "Get your API key at https://www.yaparai.com/settings "
                "and set the YAPARAI_API_KEY environment variable."
            )

        self.headers = _get_headers(self.api_key)

    async def _client(self) -> httpx.AsyncClient:
        """Return a shared async client for connection reuse."""
        global _shared_client
        if _shared_client is None or _shared_client.is_closed:
            _shared_client = httpx.AsyncClient(
                base_url=self.base_url,
                headers=self.headers,
                timeout=httpx.Timeout(30.0, connect=10.0),
            )
        return _shared_client

    async def _request(self, method: str, path: str, retries: int = 3, **kwargs) -> dict:
        """Make an HTTP request with error handling and exponential backoff retry."""
        last_exc: Exception | None = None
        for attempt in range(retries):
            try:
                client = await self._client()
                logger.debug("→ %s %s (attempt %d/%d)", method, path, attempt + 1, retries)
                resp = await client.request(method, path, **kwargs)
                logger.debug("← %s %s", resp.status_code, path)
            except httpx.ConnectError as exc:
                last_exc = exc
                if attempt < retries - 1:
                    wait = (2 ** attempt) + random.uniform(0, 1)
                    logger.warning("Connection error, retrying in %.1fs…", wait)
                    await asyncio.sleep(wait)
                    continue
                raise ConnectionError(
                    f"Cannot connect to YaparAI API at {self.base_url}. "
                    "Check your internet connection."
                ) from exc
            except httpx.TimeoutException as exc:
                last_exc = exc
                if attempt < retries - 1:
                    wait = (2 ** attempt) + random.uniform(0, 1)
                    logger.warning("Timeout, retrying in %.1fs…", wait)
                    await asyncio.sleep(wait)
                    continue
                raise TimeoutError(
                    "YaparAI API request timed out. The service may be busy — try again."
                ) from exc

            if resp.status_code == 401:
                raise PermissionError(
                    "Invalid API key. Check your YAPARAI_API_KEY or generate "
                    "a new one at https://www.yaparai.com/settings"
                )
            if resp.status_code == 402:
                raise RuntimeError(
                    "Insufficient credits. Top up at https://www.yaparai.com/pricing"
                )
            if resp.status_code == 403:
                raise PermissionError(
                    "Access denied. You may not have permission for this resource."
                )
            if resp.status_code == 429:
                # Rate limit — retry with longer backoff
                if attempt < retries - 1:
                    wait = 5 * (attempt + 1)
                    logger.warning("Rate limited, retrying in %ds…", wait)
                    await asyncio.sleep(wait)
                    continue
                raise RuntimeError(
                    "Rate limit exceeded. Please wait a moment and try again."
                )

            resp.raise_for_status()
            return resp.json()

        raise RuntimeError("Request failed after all retries.") from last_exc

    # ── Public API ──────────────────────────────────────────────

    async def generate(self, request: dict) -> dict:
        """Start a generation job."""
        return await self._request("POST", "/v1/public/generate", json=request)

    async def get_job(self, job_id: str) -> dict:
        """Get job status and result."""
        return await self._request("GET", f"/v1/public/jobs/{job_id}")

    async def get_balance(self) -> dict:
        """Get credit balance."""
        return await self._request("GET", "/v1/public/balance")

    async def get_models(self) -> dict:
        """List available models and their credit costs."""
        return await self._request("GET", "/v1/public/models")

    async def wait_for_result(
        self,
        job_id: str,
        timeout: int = 120,
        poll_interval: int = 3,
    ) -> dict:
        """Poll job status until completed or timeout."""
        elapsed = 0
        while elapsed < timeout:
            job = await self.get_job(job_id)
            status = job.get("status", "")
            if status == "succeeded":
                return job
            if status == "failed":
                error = job.get("error_message") or job.get("error") or "Unknown error"
                raise RuntimeError(f"Generation failed: {error}")
            await asyncio.sleep(poll_interval)
            elapsed += poll_interval
        raise TimeoutError(
            f"Job {job_id} is still processing after {timeout}s. "
            f"Use get_job_status('{job_id}') to check later."
        )

    # ── Templates ───────────────────────────────────────────────

    async def list_templates(self, params: dict | None = None) -> dict:
        """List ComfyUI templates."""
        return await self._request("GET", "/v1/comfy-templates", params=params)

    async def get_template(self, slug: str) -> dict:
        """Get template detail."""
        return await self._request("GET", f"/v1/comfy-templates/{slug}")

    async def execute_template(self, slug: str, payload: dict) -> dict:
        """Execute a ComfyUI template."""
        return await self._request("POST", f"/v1/comfy-templates/{slug}/execute", json=payload)

    # ── AI Providers ────────────────────────────────────────────

    async def gemini_generate(self, payload: dict) -> dict:
        """Gemini text generation."""
        return await self._request("POST", "/v1/ai/gemini/generate", json=payload)

    async def gemini_analyze_image(self, payload: dict) -> dict:
        """Gemini Vision image analysis."""
        return await self._request("POST", "/v1/ai/gemini/analyze-image", json=payload)

    # ── Chatbot ─────────────────────────────────────────────────

    async def list_chatbots(self) -> list:
        """List active chatbots."""
        return await self._request("GET", "/v1/chatbot/list")

    async def chat_sync(self, slug: str, payload: dict) -> dict:
        """Non-streaming chat with a chatbot."""
        return await self._request("POST", f"/v1/chatbot/{slug}/chat/sync", json=payload)

    # ── Enterprise: Organizations ───────────────────────────────

    async def list_organizations(self) -> list:
        """List user's organizations."""
        return await self._request("GET", "/api/enterprise/organizations")

    # ── Enterprise: Social Media ────────────────────────────────

    async def social_create_post(self, org_id: str, payload: dict) -> dict:
        """Create a social media post."""
        return await self._request(
            "POST", f"/api/enterprise/orgs/{org_id}/social/posts", json=payload
        )

    async def social_list_posts(self, org_id: str, params: dict | None = None) -> dict:
        """List social media posts."""
        return await self._request(
            "GET", f"/api/enterprise/orgs/{org_id}/social/posts", params=params
        )

    async def social_generate_caption(self, org_id: str, payload: dict) -> dict:
        """Generate AI caption for social post."""
        return await self._request(
            "POST", f"/api/enterprise/orgs/{org_id}/social/caption/generate", json=payload
        )

    async def social_generate_hashtags(self, org_id: str, payload: dict) -> dict:
        """Generate AI hashtags."""
        return await self._request(
            "POST", f"/api/enterprise/orgs/{org_id}/social/hashtags/generate", json=payload
        )

    async def social_list_accounts(self, org_id: str) -> list:
        """List connected social accounts."""
        return await self._request(
            "GET", f"/api/enterprise/orgs/{org_id}/social/accounts"
        )

    async def social_list_inbox(self, org_id: str) -> list:
        """List inbox conversations."""
        return await self._request(
            "GET", f"/api/enterprise/orgs/{org_id}/social/inbox"
        )

    async def social_get_conversation(self, org_id: str, conv_id: str, account_id: str) -> dict:
        """Get conversation messages."""
        return await self._request(
            "GET",
            f"/api/enterprise/orgs/{org_id}/social/inbox/{conv_id}",
            params={"account_id": account_id},
        )

    async def social_reply(self, org_id: str, conv_id: str, account_id: str, payload: dict) -> dict:
        """Reply to a conversation."""
        return await self._request(
            "POST",
            f"/api/enterprise/orgs/{org_id}/social/inbox/{conv_id}/reply",
            params={"account_id": account_id},
            json=payload,
        )

    async def social_ai_reply(self, org_id: str, conv_id: str, account_id: str, payload: dict) -> dict:
        """Get AI reply suggestion."""
        return await self._request(
            "POST",
            f"/api/enterprise/orgs/{org_id}/social/inbox/{conv_id}/ai-reply",
            params={"account_id": account_id},
            json=payload,
        )

    async def social_get_quota(self, org_id: str) -> dict:
        """Get social media quota."""
        return await self._request(
            "GET", f"/api/enterprise/orgs/{org_id}/social/quota"
        )

    # ── Enterprise: CRM ─────────────────────────────────────────

    async def crm_list_customers(self, org_id: str, params: dict | None = None) -> dict:
        """List CRM customers."""
        return await self._request(
            "GET", f"/api/enterprise/orgs/{org_id}/crm/customers", params=params
        )

    async def crm_get_customer(self, org_id: str, customer_id: str) -> dict:
        """Get customer details."""
        return await self._request(
            "GET", f"/api/enterprise/orgs/{org_id}/crm/customers/{customer_id}"
        )

    async def crm_extract_info(self, org_id: str, customer_id: str) -> dict:
        """Extract customer info from conversations via AI."""
        return await self._request(
            "POST", f"/api/enterprise/orgs/{org_id}/crm/customers/{customer_id}/extract-info"
        )

    async def crm_send_shipping(self, org_id: str, customer_id: str, payload: dict) -> dict:
        """Send shipping/tracking notification."""
        return await self._request(
            "POST",
            f"/api/enterprise/orgs/{org_id}/crm/customers/{customer_id}/send-shipping",
            json=payload,
        )

    async def crm_bulk_message(self, org_id: str, payload: dict) -> dict:
        """Send bulk message to customers."""
        return await self._request(
            "POST", f"/api/enterprise/orgs/{org_id}/crm/bulk-message", json=payload
        )

    async def crm_sync_from_inbox(self, org_id: str) -> dict:
        """Import customers from inbox conversations."""
        return await self._request(
            "POST", f"/api/enterprise/orgs/{org_id}/crm/sync-from-inbox"
        )
