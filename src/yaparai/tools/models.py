"""Model listing tools."""

from __future__ import annotations

from yaparai.client import YaparAIClient


async def list_models() -> dict:
    """
    List all available AI generation models and their credit costs.

    Returns a list of models with their mode identifier,
    description, credit cost, and type (image/video/music).

    Useful for understanding what you can generate and how much it costs.
    No credits are charged for this operation.
    """
    client = YaparAIClient()
    return await client.get_models()
