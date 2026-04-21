"""Tests for CRM tools."""
from __future__ import annotations
import pytest
from unittest.mock import AsyncMock, patch
from yaparai.tools.crm import bulk_message


@pytest.mark.asyncio
async def test_bulk_message_by_ids():
    with patch("yaparai.tools.crm.YaparAIClient") as M, \
         patch("yaparai.tools.crm.resolve_org_id", return_value="org1"):
        inst = M.return_value
        inst.crm_bulk_message = AsyncMock(return_value={"sent": 3, "failed": 0})
        await bulk_message(message="Hi!", customer_ids=["c1", "c2"])
        payload = inst.crm_bulk_message.call_args[0][1]
        assert payload["customer_ids"] == ["c1", "c2"]
        assert "tag" not in payload


@pytest.mark.asyncio
async def test_bulk_message_by_tag():
    with patch("yaparai.tools.crm.YaparAIClient") as M, \
         patch("yaparai.tools.crm.resolve_org_id", return_value="org1"):
        inst = M.return_value
        inst.crm_bulk_message = AsyncMock(return_value={"sent": 5, "failed": 0})
        await bulk_message(message="VIP offer!", tag="vip")
        payload = inst.crm_bulk_message.call_args[0][1]
        assert payload["tag"] == "vip"
        assert "customer_ids" not in payload


@pytest.mark.asyncio
async def test_bulk_message_by_platform():
    with patch("yaparai.tools.crm.YaparAIClient") as M, \
         patch("yaparai.tools.crm.resolve_org_id", return_value="org1"):
        inst = M.return_value
        inst.crm_bulk_message = AsyncMock(return_value={"sent": 2, "failed": 0})
        await bulk_message(message="promo", platform="instagram")
        payload = inst.crm_bulk_message.call_args[0][1]
        assert payload["platform"] == "instagram"
