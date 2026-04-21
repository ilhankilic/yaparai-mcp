"""Tests for social media tools."""
from __future__ import annotations
import pytest
from unittest.mock import AsyncMock, patch
from yaparai.tools.social import create_social_post, list_social_posts, get_social_quota


@pytest.mark.asyncio
async def test_create_post_scheduled_at():
    with patch("yaparai.tools.social.YaparAIClient") as M, \
         patch("yaparai.tools.social.resolve_org_id", return_value="org1"):
        inst = M.return_value
        inst.social_create_post = AsyncMock(return_value={"post_id": "p1", "status": "scheduled"})
        await create_social_post(
            text="Hello!", platform="instagram", account_id="acc1",
            scheduled_at="2026-05-01T10:00:00Z",
        )
        payload = inst.social_create_post.call_args[0][1]
        assert payload["scheduled_at"] == "2026-05-01T10:00:00Z"


@pytest.mark.asyncio
async def test_create_post_immediate_no_scheduled_at():
    with patch("yaparai.tools.social.YaparAIClient") as M, \
         patch("yaparai.tools.social.resolve_org_id", return_value="org1"):
        inst = M.return_value
        inst.social_create_post = AsyncMock(return_value={"post_id": "p2"})
        await create_social_post(text="Hi", platform="facebook", account_id="acc2")
        payload = inst.social_create_post.call_args[0][1]
        assert "scheduled_at" not in payload


@pytest.mark.asyncio
async def test_list_social_posts_with_platform_filter():
    with patch("yaparai.tools.social.YaparAIClient") as M, \
         patch("yaparai.tools.social.resolve_org_id", return_value="org1"):
        inst = M.return_value
        inst.social_list_posts = AsyncMock(return_value={"posts": []})
        await list_social_posts(platform="instagram")
        params = inst.social_list_posts.call_args[0][1]
        assert params["platform"] == "instagram"


@pytest.mark.asyncio
async def test_get_social_quota():
    with patch("yaparai.tools.social.YaparAIClient") as M, \
         patch("yaparai.tools.social.resolve_org_id", return_value="org1"):
        inst = M.return_value
        inst.social_get_quota = AsyncMock(return_value={"used": 10, "limit": 100})
        result = await get_social_quota()
        assert result["limit"] == 100
