"""Balance and account tools."""

from __future__ import annotations

from yaparai.client import YaparAIClient


async def check_balance() -> dict:
    """
    Check your YaparAI credit balance.

    Returns your current credit balance, total credits used,
    and the currency (credits).

    No credits are charged for this operation.
    """
    client = YaparAIClient()
    return await client.get_balance()
