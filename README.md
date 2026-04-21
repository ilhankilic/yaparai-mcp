# YaparAI MCP Server

All-in-one AI content creation + enterprise social media, CRM & competitor intel — directly from **Claude Desktop**, **Cursor**, **Windsurf**, and other MCP-compatible AI assistants.

[![PyPI](https://img.shields.io/pypi/v/yaparai)](https://pypi.org/project/yaparai/)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](LICENSE)
[![Python](https://img.shields.io/pypi/pyversions/yaparai)](https://pypi.org/project/yaparai/)
[![Tests](https://img.shields.io/badge/tests-32%20passing-brightgreen)](tests/)

## What is YaparAI?

[YaparAI](https://www.yaparai.com) is an all-in-one AI platform with **43 tools** across content generation, e-commerce, and enterprise operations:

- **Image Generation** — Flux, SDXL, Imagen 4 (text-to-image, image-to-image)
- **Video Generation** — Veo 3.1, Kling (text-to-video, image-to-video)
- **Music Generation** — Suno v4 (full songs with vocals, instrumentals)
- **Image Editing** — Background removal, face swap, style transfer
- **E-commerce** — Virtual try-on, AI mannequin for product photos
- **448+ Templates** — Pre-built ComfyUI workflows (logos, ads, product photos...)
- **AI Text & Vision** — Gemini-powered text generation and image analysis
- **Chatbots** — Interact with AI chatbots via API
- **Social Media** — Post, caption, hashtag, inbox, AI auto-reply, quota (Enterprise)
- **CRM** — Customer management, AI info extraction, shipping, bulk messaging (Enterprise)
- **Competitor Analysis** — Track competitors, compare KPIs, SWOT snapshots (Enterprise, v0.5.0)
- **Product Catalog** — Org product CRUD, stock management (Enterprise, v0.5.0)

## Quick Start

### 1. Install

```bash
pip install yaparai
```

### 2. Get your API Key

1. Sign up at [yaparai.com](https://www.yaparai.com) (100 free credits)
2. Go to **Settings > API Anahtarları**
3. **Choose scope**:
   - **Personal** — your credits, your data (default)
   - **Enterprise** — if you're a member of an organization, select it to enable
     competitor/product/inbox/CRM tools scoped to that org
4. Create the key and copy it (shown only once!)

### 3. Configure Claude Desktop

Edit your Claude Desktop config (`Settings > Developer > Edit Config`):

```json
{
  "mcpServers": {
    "yaparai": {
      "command": "yaparai",
      "env": {
        "YAPARAI_API_KEY": "yap_live_your_key_here"
      }
    }
  }
}
```

> **Org-bound keys (v0.5.0+)** — if your key is bound to an organization
> during creation, enterprise tools (competitors, products, inbox, CRM) automatically
> use that org. The old `YAPARAI_ORG_ID` env var is **optional** — only needed if
> you want to override the bound org or use a personal key for enterprise actions.

### 4. Use it!

```
> "Generate an image of a sunset over Istanbul"
> "List available templates for logo design"
> "Which competitors have the lowest PageSpeed score?"
> "Add a new product to our catalog: Summer T-Shirt, 149 TL"
> "Show me unread DMs on Instagram"
> "Send shipping info to customer #123 — Yurtiçi, tracking ABC456"
```

## Available Tools (43)

### Content Generation (4)

| Tool | Description | Cost |
|------|-------------|------|
| `generate_image` | Flux / SDXL / Imagen 4 (`model="auto"` or explicit) | ~6 credits |
| `generate_video` | Veo 3.1 or Kling (text-to-video, image-to-video) | ~350 credits |
| `generate_music` | Suno v4 (vocals or instrumental) | ~14 credits |
| `generate_music_video` | Music + video combined | ~364 credits |

### Image Editing (3)

| Tool | Description | Cost |
|------|-------------|------|
| `transform_image` | Image-to-image style transfer | ~6 credits |
| `remove_background` | `output_format="transparent"` or `"white"` | ~2 credits |
| `swap_face` | Face swap — `image_url` (target) + `face_url` (source) | ~6 credits |

### E-commerce (2)

| Tool | Description | Cost |
|------|-------------|------|
| `virtual_try_on` | Virtual clothing try-on | ~6 credits |
| `generate_mannequin` | AI mannequin for product photos | ~6 credits |

### Avatar (1)

| Tool | Description | Cost |
|------|-------------|------|
| `lip_sync` | Talking avatar from photo | ~14 credits |

### Templates (3)

| Tool | Description | Cost |
|------|-------------|------|
| `list_templates` | Browse 448+ templates | Free |
| `get_template_detail` | Get template inputs/details | Free |
| `execute_template` | Run template (supports `extra_inputs` for template-specific fields) | Varies |

### AI Tools (2)

| Tool | Description | Cost |
|------|-------------|------|
| `generate_text` | Gemini text generation (scripts, lyrics, storyboard) | ~2 credits |
| `analyze_image` | Gemini Vision image analysis | ~2 credits |

### Chatbot (2)

| Tool | Description | Cost |
|------|-------------|------|
| `list_chatbots` | List available chatbots | Free |
| `chat_with_bot` | Chat with a YaparAI chatbot | Varies |

### Enterprise: Social Media (10)

Requires an enterprise API key (org-bound) or `YAPARAI_ORG_ID`.

| Tool | Description | Cost |
|------|-------------|------|
| `list_social_accounts` | List connected social accounts | Free |
| `create_social_post` | Post to Instagram/Facebook/TikTok/X (supports `scheduled_at`) | Free |
| `list_social_posts` | **v0.4.0** — list published & scheduled posts | Free |
| `get_social_quota` | **v0.4.0** — check platform quota & usage | Free |
| `generate_caption` | AI-generate post caption | Free |
| `generate_hashtags` | AI-generate hashtags | Free |
| `list_inbox` | Read social media inbox/DMs | Free |
| `read_conversation` | Read conversation messages | Free |
| `reply_to_message` | Reply to a DM/message | Free |
| `ai_reply_suggestion` | Get AI-suggested reply | Free |

### Enterprise: CRM (6)

| Tool | Description | Cost |
|------|-------------|------|
| `list_customers` | Browse CRM customers (filter by platform/tag) | Free |
| `get_customer` | Get customer details | Free |
| `extract_customer_info` | AI-extract info from conversations | Free |
| `send_shipping_info` | Send tracking notification | Free |
| `bulk_message` | Mass message — supports `tag`/`platform` filters (v0.4.0) | Free |
| `sync_customers_from_inbox` | Import customers from inbox | Free |

### Enterprise: Competitor Analysis — **v0.5.0** (3)

| Tool | Description | Cost |
|------|-------------|------|
| `list_competitors` | List tracked competitors (PageSpeed, followers, product count) | Free |
| `get_competitor` | Get detailed competitor info | Free |
| `compare_competitors` | Compare 2–4 competitors — KPI snapshot for SWOT analysis | Free |

### Enterprise: Product Catalog — **v0.5.0** (3)

| Tool | Description | Cost |
|------|-------------|------|
| `list_org_products` | List org products with SKU, price, category, stock | Free |
| `create_org_product` | Add new product to catalog | Free |
| `update_product_stock` | Toggle `in_stock` / `out_of_stock` / `preorder` | Free |

### Utility (4)

| Tool | Description | Cost |
|------|-------------|------|
| `list_organizations` | List your organizations | Free |
| `check_balance` | Check credit balance | Free |
| `list_models` | List models and costs | Free |
| `get_job_status` | Check job status | Free |

## Configuration

| Env Variable | Description | Default |
|-------------|-------------|---------|
| `YAPARAI_API_KEY` | Your API key (required) | — |
| `YAPARAI_ORG_ID` | Organization ID — **optional** if your key is org-bound | — |
| `YAPARAI_BASE_URL` | API base URL | `https://api.yaparai.com` |

### Which key should I create?

| Scenario | Scope |
|---------|-------|
| Just me, for generation/editing | **Personal** — default |
| I'm part of a company on YaparAI and want enterprise tools | **Enterprise** — pick org during key creation |
| Multiple orgs, one key | Use a personal key + pass `org_id` parameter per call, or rely on `YAPARAI_ORG_ID` env |

## Cursor / Windsurf / Claude Code

Same configuration format in MCP settings:

```json
{
  "yaparai": {
    "command": "yaparai",
    "env": {
      "YAPARAI_API_KEY": "yap_live_your_key_here"
    }
  }
}
```

## Python SDK Usage

```python
import asyncio
from yaparai.client import YaparAIClient

async def main():
    client = YaparAIClient(api_key="yap_live_your_key_here")

    # Generate an image
    job = await client.generate({"type": "image", "prompt": "A futuristic city"})
    result = await client.wait_for_result(job["job_id"])
    print(result["result_url"])

    # Compare competitors (v0.5.0 — org-bound API key)
    comparison = await client.enterprise_compare_competitors(
        ["uuid-1", "uuid-2", "uuid-3"]
    )
    print(comparison)

    # Add a product (v0.5.0)
    product = await client.enterprise_create_org_product({
        "name": "Summer T-Shirt",
        "price": 149,
        "stock_status": "in_stock",
        "category": "apparel",
    })
    print(product)

asyncio.run(main())
```

## Reliability (v0.4.0+)

- **Exponential backoff retry** — 3 retries on network errors (1s → 2s → 4s + jitter), rate-limit aware (429 → 5s/10s/15s)
- **Literal type annotations** on `platform`, `model`, `style`, `output_format` — IDE auto-complete catches wrong values early
- **Structured logging** — `logging.getLogger("yaparai")` for debug traceability
- **32 unit tests** on HTTP client, generation, editing, social, CRM, org resolution
- **CI on Python 3.10 / 3.11 / 3.12** + ruff lint

## Pricing

- **100 free credits** on signup (no credit card required)
- Image: ~6 credits (~$0.50)
- Video: ~350 credits (~$3–5)
- Music: ~14 credits (~$1)
- Enterprise features: included with subscription
- Credits never expire

[View pricing](https://www.yaparai.com/pricing)

## Links

- **Website**: [yaparai.com](https://www.yaparai.com)
- **Enterprise Portal**: [kurumsal.yaparai.com](https://kurumsal.yaparai.com)
- **Gallery**: [yaparai.com/gallery](https://www.yaparai.com/gallery)
- **API Keys**: [yaparai.com/settings](https://www.yaparai.com/settings) (personal) · [kurumsal.yaparai.com/settings?tab=api-keys](https://kurumsal.yaparai.com/settings?tab=api-keys) (org-bound)
- **Support**: destek@yaparai.com

## Release Notes

- **v0.5.0** (2026-04-21) — 6 new enterprise tools (competitor analysis + product catalog), org-bound API keys
- **v0.4.0** (2026-04-21) — 2 new tools, retry + logging, Literal types, full test suite. Community contribution by [@enis1998](https://github.com/enis1998)
- **v0.3.1** — FastMCP 3.x compatibility
- **v0.3.0** — 30 tools, full platform coverage
- **v0.2.0** — 13 tools, PyPI ready

Full history: [CHANGELOG.md](CHANGELOG.md)

## Contributors

Thanks to everyone who has contributed to YaparAI MCP!

- [@ilhankilic](https://github.com/ilhankilic) — Creator & maintainer
- [@enis1998](https://github.com/enis1998) — v0.4.0: 2 new tools, retry mechanism, type safety, test suite

Want to contribute? Check out [CONTRIBUTING.md](CONTRIBUTING.md).

## License

Apache 2.0 — see [LICENSE](LICENSE)
