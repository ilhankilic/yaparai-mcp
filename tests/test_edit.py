"""Tests for image editing tools."""
from __future__ import annotations
import pytest
from unittest.mock import AsyncMock, patch
from yaparai.tools.edit import transform_image, remove_background, swap_face
JOB = {"job_id": "j1", "credits_used": 6, "balance_remaining": 94}
DONE = {"job_id": "j1", "status": "succeeded", "result_url": "https://cdn.yaparai.com/out.png"}
@pytest.mark.asyncio
async def test_transform_image():
    with patch("yaparai.tools.edit.YaparAIClient") as M:
        inst = M.return_value
        inst.generate = AsyncMock(return_value=JOB)
        inst.wait_for_result = AsyncMock(return_value=DONE)
        result = await transform_image("oil painting style", "https://example.com/src.jpg")
        assert result["status"] == "success"
        assert result["image_url"] == DONE["result_url"]
        payload = inst.generate.call_args[0][0]
        assert payload["mode"] == "img2img"
@pytest.mark.asyncio
async def test_remove_background_no_prompt():
    """remove_background should NOT send a prompt field."""
    job = {"job_id": "j2", "credits_used": 2, "balance_remaining": 92}
    done = {**DONE, "job_id": "j2"}
    with patch("yaparai.tools.edit.YaparAIClient") as M:
        inst = M.return_value
        inst.generate = AsyncMock(return_value=job)
        inst.wait_for_result = AsyncMock(return_value=done)
        await remove_background("https://example.com/product.jpg")
        payload = inst.generate.call_args[0][0]
        assert "prompt" not in payload
        assert payload["mode"] == "editor_bg_remove"
@pytest.mark.asyncio
async def test_remove_background_output_format():
    job = {"job_id": "j2", "credits_used": 2, "balance_remaining": 92}
    done = {**DONE, "job_id": "j2"}
    with patch("yaparai.tools.edit.YaparAIClient") as M:
        inst = M.return_value
        inst.generate = AsyncMock(return_value=job)
        inst.wait_for_result = AsyncMock(return_value=done)
        await remove_background("https://example.com/img.jpg", output_format="white")
        payload = inst.generate.call_args[0][0]
        assert payload["output_format"] == "white"
@pytest.mark.asyncio
async def test_swap_face_sends_both_urls():
    """swap_face must send both image_url and face_url."""
    with patch("yaparai.tools.edit.YaparAIClient") as M:
        inst = M.return_value
        inst.generate = AsyncMock(return_value=JOB)
        inst.wait_for_result = AsyncMock(return_value=DONE)
        await swap_face(
            image_url="https://example.com/target.jpg",
            face_url="https://example.com/face.jpg",
        )
        payload = inst.generate.call_args[0][0]
        assert payload["image_url"] == "https://example.com/target.jpg"
        assert payload["face_url"] == "https://example.com/face.jpg"
        assert payload["mode"] == "editor_face_swap"
