# Changelog

All notable changes to this project will be documented here.

Format: [Keep a Changelog](https://keepachangelog.com/en/1.0.0/)

---

## [0.5.1] — 2026-04-21 (Docs refresh)

### Changed
- **README overhaul** — full v0.4.0 + v0.5.0 tool tables with per-tool descriptions
- Added "Release Notes" section with version timeline
- Clarified org-bound API key workflow: personal vs enterprise scope, setup table
- Updated Python SDK examples with v0.5.0 `enterprise_*` client methods
- Added Reliability section (retry, logging, tests, CI) introduced in v0.4.0
- Tests badge (32 passing), link to new enterprise key page on kurumsal portal

No code changes — package identical to v0.5.0.

---

## [0.5.0] — 2026-04-21 (Enterprise High Priority)

### Added (6 new enterprise tools: 37 → 43)

**Competitor Analysis** (Sprint CA)
- `list_competitors` — list competitors tracked under your org
- `get_competitor` — detailed info for a single competitor
- `compare_competitors` — 2–4 competitor KPI snapshots for SWOT/positioning

**Product Catalog** (Sprint AD)
- `list_org_products` — org product list with SKU, price, category, stock
- `create_org_product` — add new product with full metadata
- `update_product_stock` — toggle in_stock / out_of_stock / preorder

### Changed
- **Org-bound API keys**: API keys can now be bound to an organization on creation
  (at yaparai.com/settings). When bound, enterprise tools use that org automatically;
  `YAPARAI_ORG_ID` env var is no longer required.
- Client gained `enterprise_*` methods that use `/v1/public/enterprise/*` endpoints
  with automatic `X-Organization-Id` header propagation.

### Backend
- Migration 0086: `user_api_keys.organization_id` nullable FK
- New `/v1/public/enterprise/*` route family (12 endpoints incl. inbox + CRM)
- `get_current_user_and_org` dependency with `UserWithOrg` context wrapper

---

## [0.4.0] — 2026-04-21

Community contribution by [@enis1998](https://github.com/enis1998).

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

