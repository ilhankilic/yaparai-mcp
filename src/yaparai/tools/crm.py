"""Enterprise CRM (Customer Relationship Management) tools."""

from __future__ import annotations

from typing import Literal

from yaparai.tools._org import resolve_org_id
from yaparai.client import YaparAIClient


async def list_customers(
    search: str | None = None,
    platform: Literal["instagram", "facebook", "whatsapp"] | None = None,
    tag: str | None = None,
    org_id: str | None = None,
) -> dict:
    """
    List CRM customers with optional filtering.

    Browse your customer database built from social media conversations.
    Supports search, platform filtering, and tag-based filtering.
    Requires enterprise subscription. No credits charged.

    Args:
        search: Search by customer name, email, or phone
        platform: Filter by platform ("instagram", "facebook", "whatsapp")
        tag: Filter by customer tag (e.g., "vip", "lead", "returning")
        org_id: Organization ID (uses YAPARAI_ORG_ID env var if not provided)

    Returns:
        Paginated list of customers with name, platform, contact info,
        tags, last interaction date.
    """
    oid = resolve_org_id(org_id)
    client = YaparAIClient()
    params: dict = {}
    if search:
        params["search"] = search
    if platform:
        params["platform"] = platform
    if tag:
        params["tag"] = tag
    return await client.crm_list_customers(oid, params or None)


async def get_customer(
    customer_id: str,
    org_id: str | None = None,
) -> dict:
    """
    Get detailed customer information.

    Returns full customer profile including contact details, tags,
    notes, conversation history, and order info.

    Args:
        customer_id: Customer ID (from list_customers results)
        org_id: Organization ID (uses YAPARAI_ORG_ID env var if not provided)

    Returns:
        Dict with customer details: name, phone, email, address, tags,
        notes, platform, avatar_url, created_at, last_interaction.
    """
    oid = resolve_org_id(org_id)
    client = YaparAIClient()
    return await client.crm_get_customer(oid, customer_id)


async def extract_customer_info(
    customer_id: str,
    org_id: str | None = None,
) -> dict:
    """
    Extract contact information from conversation history using AI.

    The AI reads through all messages with this customer and extracts
    their name, phone number, email address, and physical address.
    Great for auto-filling CRM records from chat conversations.

    Args:
        customer_id: Customer ID to extract info for
        org_id: Organization ID (uses YAPARAI_ORG_ID env var if not provided)

    Returns:
        Dict with extracted info: name, phone, email, address.
    """
    oid = resolve_org_id(org_id)
    client = YaparAIClient()
    return await client.crm_extract_info(oid, customer_id)


async def send_shipping_info(
    customer_id: str,
    carrier: str,
    tracking_code: str,
    org_id: str | None = None,
) -> dict:
    """
    Send shipping/tracking information to a customer via social media.

    Automatically sends a tracking message through the same social
    platform the customer contacted you on.

    Args:
        customer_id: Customer ID to notify
        carrier: Shipping carrier (e.g., "Yurtici", "Aras", "PTT", "MNG", "DHL")
        tracking_code: Package tracking number
        org_id: Organization ID (uses YAPARAI_ORG_ID env var if not provided)

    Returns:
        Dict with delivery status, carrier, and tracking_code.
    """
    oid = resolve_org_id(org_id)
    client = YaparAIClient()
    return await client.crm_send_shipping(oid, customer_id, {
        "carrier": carrier,
        "tracking_code": tracking_code,
    })


async def bulk_message(
    message: str,
    customer_ids: list[str] | None = None,
    tag: str | None = None,
    platform: Literal["instagram", "facebook", "whatsapp"] | None = None,
    media_urls: list[str] | None = None,
    org_id: str | None = None,
) -> dict:
    """
    Send a message to multiple customers at once.

    Broadcast promotions, announcements, or updates to a list of
    customers via their respective social platforms. You can target by
    specific IDs, a customer tag, or a platform.

    Args:
        message: Message text to send
        customer_ids: List of specific customer IDs to message
        tag: Send to all customers with this tag (e.g., "vip", "returning")
        platform: Send only to customers from this platform
        media_urls: Optional list of image/video URLs to attach
        org_id: Organization ID (uses YAPARAI_ORG_ID env var if not provided)

    Returns:
        Dict with sent count, failed count, and error details.
    """
    oid = resolve_org_id(org_id)
    client = YaparAIClient()
    payload: dict = {"message": message}
    if customer_ids:
        payload["customer_ids"] = customer_ids
    if tag:
        payload["tag"] = tag
    if platform:
        payload["platform"] = platform
    if media_urls:
        payload["media_urls"] = media_urls
    return await client.crm_bulk_message(oid, payload)


async def sync_customers_from_inbox(
    org_id: str | None = None,
) -> dict:
    """
    Import customers from social media inbox conversations.

    Scans all inbox conversations and creates CRM customer records
    for anyone who has messaged you. New customers are auto-tagged
    by platform. Existing customers are not duplicated.

    Args:
        org_id: Organization ID (uses YAPARAI_ORG_ID env var if not provided)

    Returns:
        Dict with status, imported count, and total conversations scanned.
    """
    oid = resolve_org_id(org_id)
    client = YaparAIClient()
    return await client.crm_sync_from_inbox(oid)
