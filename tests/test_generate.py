"""Tests for generation tools."""

from __future__ import annotations

import pytest
from unittest.mock import AsyncMock, patch

from yaparai.tools.generate import generate_image, generate_video, generate_music

JOB = {"job_id": "j1", "credits_used": 6, "balance_remaining": 94}
DONE = {"job_id": "j1", "status": "succeeded", "result_url": "https://cdn.yaparai.com/img.png"}


@pytest.mark.asyncio
async def test_generate_image_success():
    with patch("yaparai.tools.generate.YaparAIClient") as M:
        inst = M.return_value
        inst.generate = AsyncMock(return_value=JOB)
        inst.wait_for_result = AsyncMock(return_value=DONE)
        result = await generate_image("a sunset")
        assert result["status"] == "success"
        assert result["image_url"] == DONE["result_url"]


@pytest.mark.asyncio
async def test_generate_image_model_sent():
    with patch("yaparai.tools.generate.YaparAIClient") as M:
        inst = M.return_value
        inst.generate = AsyncMock(return_value=JOB)
        inst.wait_for_result = AsyncMock(return_value=DONE)
        await generate_image("a cat", model="flux")
        assert inst.generate.call_args[0][0]["model"] == "flux"


@pytest.mark.asyncio
async def test_generate_image_auto_model_not_in_payload():
    with patch("yaparai.tools.generate.YaparAIClient") as M:
        inst = M.return_value
        inst.generate = AsyncMock(return_value=JOB)
        inst.wait_for_result = AsyncMock(return_value=DONE)
        await generate_image("a dog", model="auto")
        assert "model" not in inst.generate.call_args[0][0]


@pytest.mark.asyncio
async def test_generate_video_veo_mode():
    vdone = {**DONE, "result_url": "https://cdn.yaparai.com/vid.mp4"}
    with patch("yaparai.tools.generate.YaparAIClient") as M:
        inst = M.return_value
        inst.generate = AsyncMock(return_value=JOB)
        inst.wait_for_result = AsyncMock(return_value=vdone)
        await generate_video("fly over city", model="veo")
        assert inst.generate.call_args[0][0]["mode"] == "gemini_video"


@pytest.mark.asyncio
async def test_generate_music_instrumental_prefix():
    mdone = {**DONE, "result_url": "https://cdn.yaparai.com/t.mp3"}
    with patch("yaparai.tools.generate.YaparAIClient") as M:
        inst = M.return_value
        inst.generate = AsyncMock(return_value=JOB)
        inst.wait_for_result = AsyncMock(return_value=mdone)
        await generate_music("melody", style="classical", instrumental=True)
        prompt = inst.generate.call_args[0][0]["prompt"]
        assert "[Instrumental]" in prompt
        assert "[classical]" in prompt

"""Tests for generation tools."""
