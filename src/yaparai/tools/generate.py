"""Generation tools — image, video, music."""

from __future__ import annotations

from typing import Literal

from yaparai.client import YaparAIClient


async def generate_image(
    prompt: str,
    model: Literal["auto", "flux", "sdxl", "imagen4"] = "auto",
    negative_prompt: str = "",
    width: int = 512,
    height: int = 512,
    style: Literal["realistic", "anime", "cinematic", "artistic"] | None = None,
) -> dict:
    """
    Generate an image using AI.

    Supports 3 AI models: Flux, SDXL, Imagen 4.
    Smart routing automatically picks the best model for your prompt.
    Cost: ~6 credits per image.

    Args:
        prompt: Description of the image to generate (Turkish or English)
        model: AI model to use — "auto" (smart routing), "flux" (best quality),
               "sdxl" (fast), "imagen4" (Google, photorealistic)
        negative_prompt: Things to avoid in the image
        width: Image width in pixels (64-2048, default 512)
        height: Image height in pixels (64-2048, default 512)
        style: Style preset (realistic, anime, cinematic, artistic)

    Returns:
        Dict with job_id, status, result_url (image URL when done),
        credits_used, and balance_remaining.
    """
    client = YaparAIClient()
    payload: dict = {
        "type": "image",
        "prompt": prompt,
        "negative_prompt": negative_prompt,
        "width": width,
        "height": height,
        "style": style,
    }
    if model != "auto":
        payload["model"] = model

    job = await client.generate(payload)
    result = await client.wait_for_result(job["job_id"], timeout=60)
    return {
        "status": "success",
        "image_url": result.get("result_url"),
        "job_id": result.get("job_id"),
        "credits_used": job.get("credits_used"),
        "balance_remaining": job.get("balance_remaining"),
    }


async def generate_video(
    prompt: str,
    image_url: str | None = None,
    model: Literal["auto", "veo", "kling"] = "auto",
    style: Literal["cinematic", "realistic", "artistic"] | None = None,
) -> dict:
    """
    Generate a video using AI.

    Text-to-video or image-to-video. Models: Veo 3.1, Kling.
    Cost: ~350 credits per video.

    Args:
        prompt: Description of the video to generate
        image_url: Optional source image URL (for image-to-video mode)
        model: Model to use — "auto" (default, picks best), "veo" (Veo 3.1),
            or "kling" (Kling). Veo 3.1 is best for cinematic quality.
        style: Style preset (cinematic, realistic, artistic)

    Returns:
        Dict with video_url, job_id, credits_used, and balance_remaining.
    """
    client = YaparAIClient()

    if model == "veo":
        mode = "gemini_video"
    elif image_url:
        mode = "img2video"
    else:
        mode = "text2video"

    job = await client.generate({
        "type": "video",
        "prompt": prompt,
        "mode": mode,
        "image_url": image_url,
        "style": style,
    })

    result = await client.wait_for_result(job["job_id"], timeout=180)
    return {
        "status": "success",
        "video_url": result.get("result_url"),
        "job_id": result.get("job_id"),
        "credits_used": job.get("credits_used"),
        "balance_remaining": job.get("balance_remaining"),
    }


async def generate_music(
    prompt: str,
    style: Literal["pop", "rock", "electronic", "classical", "lo-fi", "ambient"] = "pop",
    instrumental: bool = False,
) -> dict:
    """
    Generate music using AI (powered by Suno v4).

    Create full songs with vocals or instrumental tracks from text descriptions.
    Supports Turkish and English lyrics.
    Cost: ~14 credits per track.

    Args:
        prompt: Description of the music to generate (genre, mood, lyrics)
        style: Music genre (pop, rock, electronic, classical, lo-fi, ambient)
        instrumental: If True, generate without vocals

    Returns:
        Dict with job_id, status, result_url (audio URL when done),
        credits_used, and balance_remaining.
    """
    client = YaparAIClient()
    full_prompt = prompt
    if instrumental:
        full_prompt = f"[Instrumental] {prompt}"
    if style:
        full_prompt = f"[{style}] {full_prompt}"

    job = await client.generate({
        "type": "music",
        "prompt": full_prompt,
        "mode": "suno_music",
    })

    result = await client.wait_for_result(job["job_id"], timeout=120)
    return {
        "status": "success",
        "audio_url": result.get("result_url"),
        "job_id": result.get("job_id"),
        "credits_used": job.get("credits_used"),
        "balance_remaining": job.get("balance_remaining"),
    }


async def generate_music_video(
    prompt: str,
    style: Literal["pop", "rock", "electronic", "classical", "lo-fi", "ambient"] = "pop",
) -> dict:
    """
    Generate a music video — AI music + video combined.

    Creates both an original music track and a matching video in one go.
    The AI composes music and generates visuals that match the mood.
    Cost: ~364 credits (music + video).

    Args:
        prompt: Description of the music video (genre, mood, theme)
        style: Music genre (pop, rock, electronic, classical, lo-fi, ambient)

    Returns:
        Dict with video_url, job_id, credits_used, and balance_remaining.
    """
    client = YaparAIClient()
    full_prompt = f"[{style}] {prompt}" if style else prompt

    job = await client.generate({
        "type": "music",
        "prompt": full_prompt,
        "mode": "suno_music_video",
    })

    result = await client.wait_for_result(job["job_id"], timeout=180)
    return {
        "status": "success",
        "video_url": result.get("result_url"),
        "job_id": result.get("job_id"),
        "credits_used": job.get("credits_used"),
        "balance_remaining": job.get("balance_remaining"),
    }
