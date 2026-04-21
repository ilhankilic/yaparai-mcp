# YaparAI MCP Server

All-in-one AI content creation + enterprise social media & CRM — directly from **Claude Desktop**, **Cursor**, **Windsurf**, and other MCP-compatible AI assistants.

[![PyPI](https://img.shields.io/pypi/v/yaparai)](https://pypi.org/project/yaparai/)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](LICENSE)
[![Python](https://img.shields.io/pypi/pyversions/yaparai)](https://pypi.org/project/yaparai/)

## What is YaparAI?

[YaparAI](https://www.yaparai.com) is an all-in-one AI platform with 30 tools:

- **Image Generation** — Flux, SDXL, Imagen 4 (text-to-image, image-to-image)
- **Video Generation** — Veo 3.1, Kling (text-to-video, image-to-video)
- **Music Generation** — Suno v4 (full songs with vocals, instrumentals)
- **Image Editing** — Background removal, face swap, style transfer
- **E-commerce** — Virtual try-on, AI mannequin for product photos
- **448+ Templates** — Pre-built ComfyUI workflows (logos, ads, product photos...)
- **AI Text & Vision** — Gemini-powered text generation and image analysis
- **Chatbots** — Interact with AI chatbots via API
- **Social Media** — Post, caption, hashtag, inbox, AI auto-reply (Enterprise)
- **CRM** — Customer management, AI info extraction, shipping, bulk messaging (Enterprise)

## Quick Start

### 1. Install

```bash
pip install yaparai
```

### 2. Get your API Key

1. Sign up at [yaparai.com](https://www.yaparai.com) (100 free credits)
2. Go to **Settings > API Keys**
3. Create a new key — copy it (shown only once!)

### 3. Configure Claude Desktop

Edit your Claude Desktop config (`Settings > Developer > Edit Config`):

```json
{
  "mcpServers": {
    "yaparai": {
      "command": "yaparai",
      "env": {
        "YAPARAI_API_KEY": "yap_live_your_key_here",
        "YAPARAI_ORG_ID": "your-org-id-for-enterprise-features"
      }
    }
  }
}
```

> `YAPARAI_ORG_ID` is optional — only needed for social media & CRM tools.
> Use the `list_organizations` tool to find your org ID.

### 4. Use it!

> "Generate an image of a sunset over Istanbul"

> "List available templates for logo design"

> "Create a social media post for our new product launch"

> "Show me the inbox messages on Instagram"

> "Generate an AI reply for that customer question"

> "Send shipping info to customer #123 — Yurtici, tracking ABC456"

## Available Tools (30)

### Content Generation (4)

| Tool | Description | Cost |
|------|-------------|------|
| `generate_image` | Generate images (Flux, SDXL, Imagen 4) | ~6 credits |
| `generate_video` | Generate videos (Veo 3.1, Kling) | ~350 credits |
| `generate_music` | Generate music (Suno v4) | ~14 credits |
| `generate_music_video` | Music + video combined | ~364 credits |

### Image Editing (3)

| Tool | Description | Cost |
|------|-------------|------|
| `transform_image` | Image-to-image style transfer | ~6 credits |
| `remove_background` | Remove background from images | ~2 credits |
| `swap_face` | Face swap in images | ~6 credits |

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
| `execute_template` | Run a template workflow | Varies |

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

### Enterprise: Social Media (8)

| Tool | Description | Cost |
|------|-------------|------|
| `list_social_accounts` | List connected social accounts | Free |
| `create_social_post` | Post to Instagram/Facebook/TikTok/X | Free |
| `generate_caption` | AI-generate post caption | Free |
| `generate_hashtags` | AI-generate hashtags | Free |
| `list_inbox` | Read social media inbox/DMs | Free |
| `read_conversation` | Read conversation messages | Free |
| `reply_to_message` | Reply to a DM/message | Free |
| `ai_reply_suggestion` | Get AI-suggested reply | Free |

### Enterprise: CRM (6)

| Tool | Description | Cost |
|------|-------------|------|
| `list_customers` | Browse CRM customers | Free |
| `get_customer` | Get customer details | Free |
| `extract_customer_info` | AI-extract info from conversations | Free |
| `send_shipping_info` | Send tracking notification | Free |
| `bulk_message` | Mass message customers | Free |
| `sync_customers_from_inbox` | Import customers from inbox | Free |

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
| `YAPARAI_ORG_ID` | Organization ID (for enterprise tools) | — |
| `YAPARAI_BASE_URL` | API base URL | `https://api.yaparai.com` |

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

    # List templates
    templates = await client.list_templates({"category": "logo"})
    print(templates)

    # Social media caption
    caption = await client.social_generate_caption("org-id", {
        "topic": "summer sale",
        "platform": "instagram",
        "language": "tr",
    })
    print(caption)

asyncio.run(main())
```

## Pricing

- **100 free credits** on signup (no credit card required)
- Image: ~6 credits (~$0.50)
- Video: ~350 credits (~$3-5)
- Music: ~14 credits (~$1)
- Enterprise features: included with subscription
- Credits never expire

[View pricing](https://www.yaparai.com/pricing)

## Links

- **Website**: [yaparai.com](https://www.yaparai.com)
- **Enterprise**: [kurumsal.yaparai.com](https://kurumsal.yaparai.com)
- **Gallery**: [yaparai.com/gallery](https://www.yaparai.com/gallery)
- **API Keys**: [yaparai.com/settings](https://www.yaparai.com/settings)
- **Support**: destek@yaparai.com

## License

Apache 2.0 — see [LICENSE](LICENSE)
