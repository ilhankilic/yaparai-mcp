"""E-commerce AI tools — virtual try-on, AI mannequin."""

from __future__ import annotations

from yaparai.client import YaparAIClient


async def virtual_try_on(
    prompt: str,
    image_url: str,
) -> dict:
    """
    Virtual clothing try-on using AI.

    Upload a photo of a person and describe the clothing to try on.
    The AI will generate a realistic image of the person wearing
    the described outfit. Perfect for e-commerce and fashion.
    Cost: ~6 credits.

    Args:
        prompt: Description of the clothing to try on
            (e.g., "red summer dress", "blue denim jacket")
        image_url: URL of the person's photo

    Returns:
        Dict with image_url (try-on result), job_id, credits_used,
        and balance_remaining.
    """
    client = YaparAIClient()
    job = await client.generate({
        "type": "image",
        "mode": "kiyafet_deneme",
        "prompt": prompt,
        "image_url": image_url,
    })

    result = await client.wait_for_result(job["job_id"], timeout=90)
    return {
        "status": "success",
        "image_url": result.get("result_url"),
        "job_id": result.get("job_id"),
        "credits_used": job.get("credits_used"),
        "balance_remaining": job.get("balance_remaining"),
    }


async def generate_mannequin(
    prompt: str,
    image_url: str,
) -> dict:
    """
    Generate an AI mannequin / model photo for products.

    Upload a product image (clothing, accessory) and the AI will
    generate a realistic mannequin/model wearing or displaying it.
    Great for e-commerce product listings.
    Cost: ~6 credits.

    Args:
        prompt: Description of the desired mannequin/model
            (e.g., "young woman, studio lighting", "male model, outdoor setting")
        image_url: URL of the product image

    Returns:
        Dict with image_url (mannequin image), job_id, credits_used,
        and balance_remaining.
    """
    client = YaparAIClient()
    job = await client.generate({
        "type": "image",
        "mode": "manken_uret",
        "prompt": prompt,
        "image_url": image_url,
    })

    result = await client.wait_for_result(job["job_id"], timeout=90)
    return {
        "status": "success",
        "image_url": result.get("result_url"),
        "job_id": result.get("job_id"),
        "credits_used": job.get("credits_used"),
        "balance_remaining": job.get("balance_remaining"),
    }
