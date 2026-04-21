"""ComfyUI template discovery and execution tools."""

from __future__ import annotations

from yaparai.client import YaparAIClient


async def list_templates(
    category: str | None = None,
    media_type: str | None = None,
    search: str | None = None,
    featured: bool = False,
) -> dict:
    """
    Browse 448+ ready-made AI templates.

    Discover pre-built workflows for common tasks: logo creation,
    product photography, portrait retouching, ad generation, and more.
    Each template has predefined inputs — just fill in prompts and images.
    No credits charged for browsing.

    Args:
        category: Filter by category slug (e.g., "logo", "product", "portrait")
        media_type: Filter by output type ("image", "video")
        search: Search templates by name/description
        featured: Show only featured templates

    Returns:
        Dict with templates list (name, slug, description, credit_cost,
        category, media_type, thumbnail_url).
    """
    client = YaparAIClient()
    params = {}
    if category:
        params["category"] = category
    if media_type:
        params["media_type"] = media_type
    if search:
        params["search"] = search
    if featured:
        params["featured"] = "true"
    return await client.list_templates(params or None)


async def get_template_detail(
    slug: str,
) -> dict:
    """
    Get full details of a template including its input parameters.

    Returns the template's input fields (what you need to provide),
    output format, description, and credit cost. Use this before
    executing a template to understand its requirements.
    No credits charged.

    Args:
        slug: Template slug (from list_templates results)

    Returns:
        Dict with template details: name, description, io_inputs (required
        fields like prompt, image_url, etc.), credit_cost, and workflow info.
    """
    client = YaparAIClient()
    return await client.get_template(slug)


async def execute_template(
    slug: str,
    prompt: str,
    image_url: str | None = None,
    width: int = 512,
    height: int = 512,
    extra_inputs: dict | None = None,
) -> dict:
    """
    Execute a ComfyUI template to generate content.

    Runs a pre-built AI workflow with your inputs. Each template has
    different capabilities — use get_template_detail() first to see
    what inputs are accepted. Credits are deducted based on the template.

    Args:
        slug: Template slug (e.g., "flux-logo-generator", "product-photo-enhancer")
        prompt: Main text prompt for the template
        image_url: Input image URL (required for image-based templates)
        width: Output width in pixels (64-2048)
        height: Output height in pixels (64-2048)
        extra_inputs: Additional template-specific inputs (see get_template_detail).
                      e.g., {"brand_color": "#FF0000", "logo_text": "ACME Corp"}

    Returns:
        Dict with job_id, status, and result info.
    """
    client = YaparAIClient()
    payload: dict = {
        "prompt": prompt,
        "width": width,
        "height": height,
    }
    if image_url:
        payload["image_url"] = image_url
    if extra_inputs:
        payload.update(extra_inputs)

    result = await client.execute_template(slug, payload)

    # If the template returns a job_id, poll for result
    job_id = result.get("job_id")
    if job_id:
        final = await client.wait_for_result(job_id, timeout=120)
        return {
            "status": "success",
            "result_url": final.get("result_url"),
            "job_id": job_id,
            "credits_used": result.get("credits_used"),
            "balance_remaining": result.get("balance_remaining"),
        }

    return result
