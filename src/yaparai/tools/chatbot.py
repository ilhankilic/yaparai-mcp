"""Chatbot interaction tools."""

from __future__ import annotations

from yaparai.client import YaparAIClient


async def list_chatbots() -> dict:
    """
    List all available chatbots on YaparAI.

    Returns active chatbots with their slug, name, description,
    and configuration. Use the slug to chat with a specific bot.
    No credits charged.

    Returns:
        List of chatbot configs with slug, name, description, avatar_url.
    """
    client = YaparAIClient()
    return await client.list_chatbots()


async def chat_with_bot(
    slug: str,
    message: str,
    conversation_id: str | None = None,
) -> dict:
    """
    Send a message to a YaparAI chatbot and get a response.

    Each chatbot is specialized for different tasks (customer support,
    product recommendations, etc.). Use list_chatbots() to discover
    available bots. Provide conversation_id to continue a conversation.

    Args:
        slug: Chatbot slug (from list_chatbots results)
        message: Your message to the chatbot
        conversation_id: Optional — continue an existing conversation

    Returns:
        Dict with assistant's response text, conversation_id (for follow-ups),
        and message metadata.
    """
    client = YaparAIClient()
    payload: dict = {"messages": [{"role": "user", "content": message}]}
    if conversation_id:
        payload["conversation_id"] = conversation_id
    return await client.chat_sync(slug, payload)
