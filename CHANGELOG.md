# Changelog

All notable changes to this project will be documented here.

Format: [Keep a Changelog](https://keepachangelog.com/en/1.0.0/)

---

## [Unreleased]

### Added
- `list_social_posts` tool — list published and scheduled social media posts
- `get_social_quota` tool — check social media quota and usage limits
- `model` parameter to `generate_image` — choose between `flux`, `sdxl`, `imagen4`, or `auto`
- `scheduled_at` parameter to `create_social_post` — schedule posts for a future datetime
- `face_url` parameter to `swap_face` — provide separate source face image
- `output_format` parameter to `remove_background` — choose `transparent` or `white` output
- `extra_inputs` parameter to `execute_template` — pass template-specific additional inputs
- `tag` and `platform` filter parameters to `bulk_message` — target customers by tag or platform
- `Literal` type annotations across all tool parameters for better IDE support
- Exponential backoff retry mechanism in `YaparAIClient._request` (3 retries, rate-limit aware)
- Structured logging via Python `logging` module (`logger = logging.getLogger("yaparai")`)
- Full test suite under `tests/` with `pytest` + `pytest-asyncio` + `respx`
- GitHub Actions CI pipeline (`.github/workflows/ci.yml`) — tests on Python 3.10/3.11/3.12 + ruff lint
- `CONTRIBUTING.md` — contributor guide
- `CHANGELOG.md` — this file

### Fixed
- `remove_background` no longer requires a meaningless `prompt` parameter
- `swap_face` now correctly accepts both `image_url` (target) and `face_url` (source face)

### Changed
- `bulk_message` signature: `customer_ids` is now optional; `message` is the first positional arg
- Total registered MCP tools: 30 → 32

---

## [0.3.1] — 2026-04-01

### Initial public release
- 30 tools: image/video/music generation, editing, e-commerce, avatar, templates, AI, chatbot, social media, CRM, utility
- FastMCP-based server
- Public API + Enterprise API client

