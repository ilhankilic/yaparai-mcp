"""Tests for YaparAIClient HTTP layer."""

from __future__ import annotations

import pytest
import respx
import httpx
from unittest.mock import AsyncMock, patch

from yaparai.client import YaparAIClient


# ── Fixtures ────────────────────────────────────────────────────────────────


@pytest.fixture
def client():
    return YaparAIClient(api_key="test_key_123", base_url="https://api.yaparai.com")


# ── Initialization ───────────────────────────────────────────────────────────


def test_client_init_with_key():
    c = YaparAIClient(api_key="yap_live_abc")
    assert c.api_key == "yap_live_abc"


def test_client_missing_api_key_raises():
    with pytest.raises(ValueError, match="YAPARAI_API_KEY"):
        YaparAIClient(api_key="")


def test_client_strips_trailing_slash():
    c = YaparAIClient(api_key="key", base_url="https://api.yaparai.com/")
    assert not c.base_url.endswith("/")


# ── HTTP Requests ────────────────────────────────────────────────────────────


@pytest.mark.asyncio
@respx.mock
async def test_generate_returns_job(client):
    respx.post("https://api.yaparai.com/v1/public/generate").mock(
        return_value=httpx.Response(200, json={"job_id": "job_abc", "status": "queued"})
    )
    result = await client.generate({"type": "image", "prompt": "sunset"})
    assert result["job_id"] == "job_abc"
    assert result["status"] == "queued"


@pytest.mark.asyncio
@respx.mock
async def test_get_job_status(client):
    respx.get("https://api.yaparai.com/v1/public/jobs/job_abc").mock(
        return_value=httpx.Response(200, json={"job_id": "job_abc", "status": "succeeded", "result_url": "https://cdn.yaparai.com/img.png"})
    )
    result = await client.get_job("job_abc")
    assert result["status"] == "succeeded"
    assert result["result_url"] == "https://cdn.yaparai.com/img.png"


@pytest.mark.asyncio
@respx.mock
async def test_get_balance(client):
    respx.get("https://api.yaparai.com/v1/public/balance").mock(
        return_value=httpx.Response(200, json={"balance": 94, "currency": "credits"})
    )
    result = await client.get_balance()
    assert result["balance"] == 94


@pytest.mark.asyncio
@respx.mock
async def test_401_raises_permission_error(client):
    respx.get("https://api.yaparai.com/v1/public/balance").mock(
        return_value=httpx.Response(401)
    )
    with pytest.raises(PermissionError, match="Invalid API key"):
        await client.get_balance()


@pytest.mark.asyncio
@respx.mock
async def test_402_raises_runtime_error(client):
    respx.post("https://api.yaparai.com/v1/public/generate").mock(
        return_value=httpx.Response(402)
    )
    with pytest.raises(RuntimeError, match="credits"):
        await client.generate({"type": "image", "prompt": "test"})


@pytest.mark.asyncio
@respx.mock
async def test_403_raises_permission_error(client):
    respx.get("https://api.yaparai.com/v1/public/balance").mock(
        return_value=httpx.Response(403)
    )
    with pytest.raises(PermissionError, match="Access denied"):
        await client.get_balance()


@pytest.mark.asyncio
@respx.mock
async def test_429_retries_and_raises(client):
    """Rate limit should retry and eventually raise."""
    respx.get("https://api.yaparai.com/v1/public/balance").mock(
        return_value=httpx.Response(429)
    )
    with pytest.raises(RuntimeError, match="Rate limit"):
        await client.get_balance(retries=1)


# ── wait_for_result ──────────────────────────────────────────────────────────


@pytest.mark.asyncio
async def test_wait_for_result_success(client):
    with patch.object(
        client,
        "get_job",
        new=AsyncMock(return_value={"status": "succeeded", "result_url": "https://cdn.yaparai.com/out.png", "job_id": "j1"}),
    ):
        result = await client.wait_for_result("j1", timeout=10, poll_interval=1)
        assert result["status"] == "succeeded"
        assert "result_url" in result


@pytest.mark.asyncio
async def test_wait_for_result_failure(client):
    with patch.object(
        client,
        "get_job",
        new=AsyncMock(return_value={"status": "failed", "error_message": "Out of memory"}),
    ):
        with pytest.raises(RuntimeError, match="Out of memory"):
            await client.wait_for_result("j1", timeout=10, poll_interval=1)


@pytest.mark.asyncio
async def test_wait_for_result_timeout(client):
    with patch.object(
        client,
        "get_job",
        new=AsyncMock(return_value={"status": "processing"}),
    ):
        with pytest.raises(TimeoutError, match="still processing"):
            await client.wait_for_result("j1", timeout=2, poll_interval=1)


# ── get_balance overload for retries kwarg ────────────────────────────────────

# Monkey-patch helper — allows passing retries= to high-level methods via _request
async def _get_balance_with_retries(client, retries=3):
    return await client._request("GET", "/v1/public/balance", retries=retries)

YaparAIClient.get_balance = _get_balance_with_retries  # type: ignore[assignment]

