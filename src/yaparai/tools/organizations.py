"""Organization discovery tools."""

from __future__ import annotations

from yaparai.client import YaparAIClient


async def list_organizations() -> dict:
    """
    List your organizations on YaparAI.

    Returns organizations you're a member of, with their IDs, names,
    and your role. Use the org ID for enterprise tools (social media,
    CRM, chatbots). You can set YAPARAI_ORG_ID env var to skip
    passing org_id to every call.
    No credits charged.

    Returns:
        List of organizations with id, name, role, and member count.
    """
    client = YaparAIClient()
    return await client.list_organizations()
