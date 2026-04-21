"""AI tools — text generation, image analysis."""

from __future__ import annotations

from yaparai.client import YaparAIClient


async def generate_text(
    prompt: str,
    sub_mode: str = "script",
    temperature: float = 0.7,
    max_tokens: int = 2048,
) -> dict:
    """
    Generate text content using Gemini AI.

    Create scripts, storyboards, song lyrics, marketing copy, and more.
    Powered by Google Gemini. Cost: ~2 credits.

    Args:
        prompt: What to generate (e.g., "Write a 30-second ad script for a coffee brand")
        sub_mode: Generation mode — "script" (video/ad scripts), "storyboard"
            (visual scene descriptions), or "lyrics" (song lyrics)
        temperature: Creativity level (0.0 = focused, 1.0 = creative, default 0.7)
        max_tokens: Maximum output length (default 2048)

    Returns:
        Dict with generated text content.
    """
    client = YaparAIClient()
    return await client.gemini_generate({
        "prompt": prompt,
        "sub_mode": sub_mode,
        "temperature": temperature,
        "max_tokens": max_tokens,
    })


async def analyze_image(
    image_url: str,
    prompt: str = "Describe this image in detail",
) -> dict:
    """
    Analyze an image using Gemini Vision AI.

    Upload an image and ask questions about it. Can identify objects,
    read text, describe scenes, analyze compositions, and more.
    Cost: ~2 credits.

    Args:
        image_url: URL of the image to analyze
        prompt: Question or instruction about the image
            (e.g., "What product is shown?", "Read the text in this image")

    Returns:
        Dict with analysis text and details.
    """
    client = YaparAIClient()
    return await client.gemini_analyze_image({
        "image_url": image_url,
        "prompt": prompt,
    })
