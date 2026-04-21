"""Enterprise tools — competitor analysis + product catalog (v0.5.0).

These tools require an API key bound to an organization (or an explicit
org_id parameter). Use the "API Anahtarları" page on yaparai.com/settings
to create an org-bound key.

All enterprise endpoints are org-scoped: they only return/modify data
owned by the organization the API key is bound to.
"""

from __future__ import annotations

from typing import Literal

from yaparai.client import YaparAIClient


# ─────────────────────────────────────────────────────────────────────────────
# Competitor Analysis (Sprint CA — kurumsal rakip analizi)
# ─────────────────────────────────────────────────────────────────────────────


async def list_competitors(
    limit: int = 50,
    offset: int = 0,
    org_id: str | None = None,
) -> dict:
    """
    List competitors tracked under your organization.

    Competitor tracking includes website crawling (PageSpeed, SEO),
    social media metrics (followers, engagement), and marketplace
    product prices (Hepsiburada, Trendyol).

    Requires enterprise subscription with an org-bound API key.

    Args:
        limit: Max results (default 50)
        offset: Pagination offset
        org_id: Optional — override the org bound to the API key

    Returns:
        {"competitors": [...], "total": N} — each competitor with
        id, name, website, notes, created_at.
    """
    client = YaparAIClient()
    return await client.enterprise_list_competitors(limit=limit, offset=offset, org_id=org_id)


async def get_competitor(
    competitor_id: str,
    org_id: str | None = None,
) -> dict:
    """
    Get detailed info for a single competitor.

    Args:
        competitor_id: UUID from list_competitors results
        org_id: Optional — override the org bound to the API key

    Returns:
        Competitor profile including name, website, industry, notes.
    """
    client = YaparAIClient()
    return await client.enterprise_get_competitor(competitor_id, org_id=org_id)


async def compare_competitors(
    competitor_ids: list[str],
    org_id: str | None = None,
) -> dict:
    """
    Compare 2–4 competitors on key metrics.

    Returns latest metric snapshots for each competitor including
    PageSpeed score, total followers, posts in last 30 days, and
    product count. Use this as the basis for SWOT analysis or
    positioning decisions.

    Args:
        competitor_ids: 2–4 competitor UUIDs
        org_id: Optional — override the org bound to the API key

    Returns:
        {"metrics": [...]} — one entry per competitor with KPI snapshot.
    """
    if not 2 <= len(competitor_ids) <= 4:
        raise ValueError("competitor_ids must have 2 to 4 items")
    client = YaparAIClient()
    return await client.enterprise_compare_competitors(competitor_ids, org_id=org_id)


# ─────────────────────────────────────────────────────────────────────────────
# Product Catalog (Sprint AD — e-ticaret)
# ─────────────────────────────────────────────────────────────────────────────


async def list_org_products(
    limit: int = 50,
    offset: int = 0,
    org_id: str | None = None,
) -> dict:
    """
    List product catalog for your organization.

    Returns org's product list with SKU, price, category, image,
    stock status (in_stock / out_of_stock / preorder). Used for
    automated social media posts, chatbot product lookup, or
    inventory management from AI assistants.

    Args:
        limit: Max results (default 50)
        offset: Pagination offset
        org_id: Optional — override the org bound to the API key

    Returns:
        {"products": [...], "total": N}
    """
    client = YaparAIClient()
    return await client.enterprise_list_org_products(limit=limit, offset=offset, org_id=org_id)


async def create_org_product(
    name: str,
    sku: str | None = None,
    price: float | None = None,
    currency: str = "TRY",
    category: str | None = None,
    image_url: str | None = None,
    stock_status: Literal["in_stock", "out_of_stock", "preorder"] = "in_stock",
    description: str | None = None,
    org_id: str | None = None,
) -> dict:
    """
    Create a new product in your organization's catalog.

    Args:
        name: Product name (required)
        sku: Optional SKU / part number
        price: Optional price (numeric)
        currency: ISO currency code (default TRY)
        category: Optional category slug
        image_url: Optional product image URL (hosted image)
        stock_status: in_stock | out_of_stock | preorder
        description: Optional long description
        org_id: Optional — override the org bound to the API key

    Returns:
        Created product record (with generated id + created_at).
    """
    if not name or not name.strip():
        raise ValueError("name is required")
    payload: dict = {"name": name.strip(), "currency": currency, "stock_status": stock_status}
    if sku:
        payload["sku"] = sku
    if price is not None:
        payload["price"] = price
    if category:
        payload["category"] = category
    if image_url:
        payload["image_url"] = image_url
    if description:
        payload["description"] = description

    client = YaparAIClient()
    return await client.enterprise_create_org_product(payload, org_id=org_id)


async def update_product_stock(
    product_id: str,
    stock_status: Literal["in_stock", "out_of_stock", "preorder"],
    org_id: str | None = None,
) -> dict:
    """
    Update a product's stock status.

    Use this to quickly mark products as out of stock when inventory
    runs out, or to flip back to in_stock after restocking. For
    variant-level stock counts, see v0.6.0 roadmap.

    Args:
        product_id: UUID from list_org_products results
        stock_status: in_stock | out_of_stock | preorder
        org_id: Optional — override the org bound to the API key

    Returns:
        Updated product record.
    """
    if stock_status not in ("in_stock", "out_of_stock", "preorder"):
        raise ValueError("stock_status must be in_stock | out_of_stock | preorder")
    client = YaparAIClient()
    return await client.enterprise_update_product_stock(
        product_id, stock_status, org_id=org_id
    )
