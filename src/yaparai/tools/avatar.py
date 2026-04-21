"""Avatar and lip sync tools."""

from __future__ import annotations

from yaparai.client import YaparAIClient


async def lip_sync(
    prompt: str,
    image_url: str,
) -> dict:
    """
    Create a talking avatar from a photo using AI lip sync.

    Upload a face photo and provide the text/speech description.
    The AI will animate the face to appear as if it's speaking.
    Great for presentations, social media, and content creation.
    Cost: ~14 credits.

    Args:
        prompt: The speech or dialogue for the avatar
            (e.g., "Hello! Welcome to our channel.")
        image_url: URL of the face photo to animate

    Returns:
        Dict with video_url (animated avatar video), job_id,
        credits_used, and balance_remaining.
    """
    client = YaparAIClient()
    job = await client.generate({
        "type": "video",
        "mode": "lip_sync",
        "prompt": prompt,
        "image_url": image_url,
    })

    result = await client.wait_for_result(job["job_id"], timeout=180)
    return {
        "status": "success",
        "video_url": result.get("result_url"),
        "job_id": result.get("job_id"),
        "credits_used": job.get("credits_used"),
        "balance_remaining": job.get("balance_remaining"),
    }
