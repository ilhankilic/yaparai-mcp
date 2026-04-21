"""
YaparAI MCP Server — AI content creation + enterprise social media & CRM.

30 tools covering image/video/music generation, 448+ templates,
social media management, CRM, chatbots, and AI text/vision analysis.

Usage with Claude Desktop:
    {
        "mcpServers": {
            "yaparai": {
                "command": "yaparai",
                "env": {
                    "YAPARAI_API_KEY": "yap_live_xxxxxxxxxxxxx",
                    "YAPARAI_ORG_ID": "optional-for-enterprise"
                }
            }
        }
    }
"""

from fastmcp import FastMCP

# --- Generation ---
from yaparai.tools.generate import (
    generate_image,
    generate_video,
    generate_music,
    generate_music_video,
)

# --- Image Editing ---
from yaparai.tools.edit import (
    transform_image,
    remove_background,
    swap_face,
)

# --- E-commerce ---
from yaparai.tools.ecommerce import (
    virtual_try_on,
    generate_mannequin,
)

# --- Avatar ---
from yaparai.tools.avatar import lip_sync

# --- Templates (448+ ComfyUI workflows) ---
from yaparai.tools.templates import (
    list_templates,
    get_template_detail,
    execute_template,
)

# --- AI Tools ---
from yaparai.tools.ai import (
    generate_text,
    analyze_image,
)

# --- Chatbot ---
from yaparai.tools.chatbot import (
    list_chatbots,
    chat_with_bot,
)

# --- Enterprise: Organizations ---
from yaparai.tools.organizations import list_organizations

# --- Enterprise: Social Media ---
from yaparai.tools.social import (
    list_social_accounts,
    create_social_post,
    list_social_posts,
    get_social_quota,
    generate_caption,
    generate_hashtags,
    list_inbox,
    read_conversation,
    reply_to_message,
    ai_reply_suggestion,
)

# --- Enterprise: CRM ---
from yaparai.tools.crm import (
    list_customers,
    get_customer,
    extract_customer_info,
    send_shipping_info,
    bulk_message,
    sync_customers_from_inbox,
)

# --- Utility ---
from yaparai.tools.balance import check_balance
from yaparai.tools.models import list_models
from yaparai.tools.jobs import get_job_status

mcp = FastMCP(
    "YaparAI",
    instructions=(
        "YaparAI — all-in-one AI content creation + enterprise platform. "
        "32 tools: image/video/music generation (Flux, SDXL, Imagen 4, "
        "Veo 3.1, Kling, Suno v4), 448+ templates, image editing "
        "(background removal, face swap, virtual try-on), AI text & vision, "
        "social media management (post, caption, inbox, AI auto-reply, quota), "
        "CRM (customers, shipping, bulk messaging), and chatbot interaction. "
        "100 free credits on signup. "
        "Get your API key at https://www.yaparai.com/settings"
    ),
)

# Generation (4)
mcp.tool(generate_image)
mcp.tool(generate_video)
mcp.tool(generate_music)
mcp.tool(generate_music_video)

# Image Editing (3)
mcp.tool(transform_image)
mcp.tool(remove_background)
mcp.tool(swap_face)

# E-commerce (2)
mcp.tool(virtual_try_on)
mcp.tool(generate_mannequin)

# Avatar (1)
mcp.tool(lip_sync)

# Templates (3)
mcp.tool(list_templates)
mcp.tool(get_template_detail)
mcp.tool(execute_template)

# AI Tools (2)
mcp.tool(generate_text)
mcp.tool(analyze_image)

# Chatbot (2)
mcp.tool(list_chatbots)
mcp.tool(chat_with_bot)

# Enterprise: Organizations (1)
mcp.tool(list_organizations)

# Enterprise: Social Media (10)
mcp.tool(list_social_accounts)
mcp.tool(create_social_post)
mcp.tool(list_social_posts)
mcp.tool(get_social_quota)
mcp.tool(generate_caption)
mcp.tool(generate_hashtags)
mcp.tool(list_inbox)
mcp.tool(read_conversation)
mcp.tool(reply_to_message)
mcp.tool(ai_reply_suggestion)

# Enterprise: CRM (6)
mcp.tool(list_customers)
mcp.tool(get_customer)
mcp.tool(extract_customer_info)
mcp.tool(send_shipping_info)
mcp.tool(bulk_message)
mcp.tool(sync_customers_from_inbox)

# Utility (3)
mcp.tool(check_balance)
mcp.tool(list_models)
mcp.tool(get_job_status)


def main():
    """Entry point for the yaparai CLI command."""
    mcp.run()


if __name__ == "__main__":
    main()
