"""Enterprise social media management tools."""

from __future__ import annotations

from typing import Literal

from yaparai.tools._org import resolve_org_id
from yaparai.client import YaparAIClient

Platform = Literal["instagram", "facebook", "tiktok", "twitter"]


async def list_social_accounts(
    org_id: str | None = None,
) -> dict:
    """
    List connected social media accounts (Instagram, Facebook, TikTok, etc.).

    Shows all social accounts linked to your organization.
    Requires enterprise subscription. No credits charged.

    Args:
        org_id: Organization ID (uses YAPARAI_ORG_ID env var if not provided)

    Returns:
        List of social accounts with platform, username, account_id, and status.
    """
    oid = resolve_org_id(org_id)
    client = YaparAIClient()
    return await client.social_list_accounts(oid)


async def create_social_post(
    text: str,
    platform: Platform,
    account_id: str,
    media_urls: list[str] | None = None,
    scheduled_at: str | None = None,
    org_id: str | None = None,
) -> dict:
    """
    Create and publish a social media post.

    Post to Instagram, Facebook, TikTok, Twitter/X and other platforms.
    Supports text, images, and videos. Requires enterprise subscription.

    Args:
        text: Post caption/text content
        platform: Target platform ("instagram", "facebook", "tiktok", "twitter")
        account_id: Social account ID (from list_social_accounts)
        media_urls: Optional list of image/video URLs to attach
        scheduled_at: Optional ISO 8601 datetime to schedule the post
                      (e.g., "2026-05-01T10:00:00Z"). If None, posts immediately.
        org_id: Organization ID (uses YAPARAI_ORG_ID env var if not provided)

    Returns:
        Dict with post_id, status, platform, and published details.
    """
    oid = resolve_org_id(org_id)
    client = YaparAIClient()
    payload: dict = {
        "text": text,
        "platform": platform,
        "account_id": account_id,
    }
    if media_urls:
        payload["media_urls"] = media_urls
    if scheduled_at:
        payload["scheduled_at"] = scheduled_at
    return await client.social_create_post(oid, payload)


async def list_social_posts(
    platform: Platform | None = None,
    account_id: str | None = None,
    org_id: str | None = None,
) -> dict:
    """
    List published and scheduled social media posts.

    Returns all posts for the organization, with optional filtering
    by platform or specific account. Requires enterprise subscription.

    Args:
        platform: Filter by platform ("instagram", "facebook", "tiktok", "twitter")
        account_id: Filter by specific social account ID
        org_id: Organization ID (uses YAPARAI_ORG_ID env var if not provided)

    Returns:
        List of posts with content, platform, published_at, and engagement stats.
    """
    oid = resolve_org_id(org_id)
    client = YaparAIClient()
    params: dict = {}
    if platform:
        params["platform"] = platform
    if account_id:
        params["account_id"] = account_id
    return await client.social_list_posts(oid, params or None)


async def get_social_quota(
    org_id: str | None = None,
) -> dict:
    """
    Get social media quota and usage limits.

    Returns remaining post quota, message limits, and billing period info.
    Useful to check before running bulk operations.

    Args:
        org_id: Organization ID (uses YAPARAI_ORG_ID env var if not provided)

    Returns:
        Dict with quota limits, used counts, and billing period dates.
    """
    oid = resolve_org_id(org_id)
    client = YaparAIClient()
    return await client.social_get_quota(oid)


async def generate_caption(
    topic: str,
    platform: Platform = "instagram",
    language: Literal["tr", "en"] = "tr",
    tone: Literal["professional", "casual", "fun", "formal"] = "professional",
    org_id: str | None = None,
) -> dict:
    """
    Generate an AI-powered social media caption.

    Creates engaging, platform-optimized captions using AI.
    Supports multiple languages and tones.

    Args:
        topic: What the post is about (e.g., "new summer collection launch")
        platform: Target platform ("instagram", "facebook", "tiktok", "twitter")
        language: Caption language ("tr" for Turkish, "en" for English)
        tone: Writing tone ("professional", "casual", "fun", "formal")
        org_id: Organization ID (uses YAPARAI_ORG_ID env var if not provided)

    Returns:
        Dict with generated caption text.
    """
    oid = resolve_org_id(org_id)
    client = YaparAIClient()
    return await client.social_generate_caption(oid, {
        "topic": topic,
        "platform": platform,
        "language": language,
        "tone": tone,
    })


async def generate_hashtags(
    caption: str,
    platform: Platform = "instagram",
    language: Literal["tr", "en"] = "tr",
    org_id: str | None = None,
) -> dict:
    """
    Generate AI-optimized hashtags for a social media post.

    Creates relevant, trending hashtags based on your caption content.

    Args:
        caption: The post caption to generate hashtags for
        platform: Target platform ("instagram", "facebook", "tiktok")
        language: Hashtag language ("tr" for Turkish, "en" for English)
        org_id: Organization ID (uses YAPARAI_ORG_ID env var if not provided)

    Returns:
        Dict with list of recommended hashtags.
    """
    oid = resolve_org_id(org_id)
    client = YaparAIClient()
    return await client.social_generate_hashtags(oid, {
        "caption": caption,
        "platform": platform,
        "language": language,
    })


async def list_inbox(org_id: str | None = None) -> dict:
    """
    List social media inbox conversations (DMs, comments).

    Shows all incoming messages from Instagram, Facebook, WhatsApp, etc.
    Requires enterprise subscription. No credits charged.

    Args:
        org_id: Organization ID (uses YAPARAI_ORG_ID env var if not provided)

    Returns:
        List of conversations with sender info, last message, platform,
        and unread status.
    """
    oid = resolve_org_id(org_id)
    client = YaparAIClient()
    return await client.social_list_inbox(oid)


async def read_conversation(
    conversation_id: str,
    account_id: str,
    org_id: str | None = None,
) -> dict:
    """
    Read messages in a social media conversation.

    Get the full message history of a DM or comment thread.

    Args:
        conversation_id: Conversation ID (from list_inbox results)
        account_id: Social account ID that received the messages
        org_id: Organization ID (uses YAPARAI_ORG_ID env var if not provided)

    Returns:
        Dict with conversation messages, sender info, and timestamps.
    """
    oid = resolve_org_id(org_id)
    client = YaparAIClient()
    return await client.social_get_conversation(oid, conversation_id, account_id)


async def reply_to_message(
    conversation_id: str,
    account_id: str,
    message: str,
    org_id: str | None = None,
) -> dict:
    """
    Reply to a social media message/DM.

    Send a reply in an existing conversation on Instagram, Facebook,
    WhatsApp, or other connected platforms.

    Args:
        conversation_id: Conversation ID to reply in
        account_id: Social account ID to reply from
        message: Reply text
        org_id: Organization ID (uses YAPARAI_ORG_ID env var if not provided)

    Returns:
        Dict with reply status confirmation.
    """
    oid = resolve_org_id(org_id)
    client = YaparAIClient()
    return await client.social_reply(oid, conversation_id, account_id, {
        "message": message,
    })


async def ai_reply_suggestion(
    conversation_id: str,
    account_id: str,
    system_prompt: str = "",
    org_id: str | None = None,
) -> dict:
    """
    Get an AI-generated reply suggestion for a social media conversation.

    The AI reads the conversation context and suggests an appropriate reply.
    You can customize the AI behavior with a system prompt.

    Args:
        conversation_id: Conversation ID to suggest a reply for
        account_id: Social account ID
        system_prompt: Optional custom instructions for the AI
            (e.g., "Reply politely in Turkish, offer 10% discount")
        org_id: Organization ID (uses YAPARAI_ORG_ID env var if not provided)

    Returns:
        Dict with suggested_reply text.
    """
    oid = resolve_org_id(org_id)
    client = YaparAIClient()
    return await client.social_ai_reply(oid, conversation_id, account_id, {
        "system_prompt": system_prompt,
    })
