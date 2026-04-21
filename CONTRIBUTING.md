# Contributing to YaparAI MCP

Thank you for your interest in contributing! This guide covers everything you need to get started.

## Prerequisites

- Python 3.10+
- git

## Getting Started

```bash
# 1. Fork the repo on GitHub, then clone your fork
git clone https://github.com/<your-username>/yaparai-mcp.git
cd yaparai-mcp

# 2. Install in editable mode with dev dependencies
pip install -e ".[dev]"

# 3. Run tests to make sure everything works
pytest tests/ -v

# 4. Run linter
ruff check src/
```

## Making Changes

1. Create a new branch:
   ```bash
   git checkout -b fix/swap-face-face-url
   # or
   git checkout -b feature/list-social-posts
   ```

2. Make your changes.

3. Add or update tests in `tests/`.

4. Verify tests pass:
   ```bash
   pytest tests/ -v
   ```

5. Verify linting:
   ```bash
   ruff check src/
   ```

6. Commit and push:
   ```bash
   git add .
   git commit -m "fix: add face_url parameter to swap_face"
   git push origin fix/swap-face-face-url
   ```

7. Open a Pull Request to `ilhankilic/yaparai-mcp`.

## Commit Message Format

Use the [Conventional Commits](https://www.conventionalcommits.org/) style:

| Prefix | When to use |
|--------|-------------|
| `feat:` | New feature or tool |
| `fix:` | Bug fix |
| `docs:` | Documentation only |
| `test:` | Adding or fixing tests |
| `refactor:` | Code change without new feature/fix |
| `chore:` | Build system, dependencies |

## Code Style

- Follow existing code style (async functions, type hints, docstrings)
- Use `Literal` types for constrained string parameters
- All public functions must have docstrings with `Args` and `Returns` sections
- Keep tool functions thin — business logic belongs in `client.py`

## Project Structure

```
src/yaparai/
├── client.py       # HTTP layer — add new API methods here
├── config.py       # Environment variables
├── server.py       # FastMCP registration — register new tools here
└── tools/
    ├── generate.py  # Content generation
    ├── edit.py      # Image editing
    ├── social.py    # Social media (enterprise)
    ├── crm.py       # CRM (enterprise)
    └── ...
```

## Adding a New Tool

1. Add the API method in `client.py`
2. Create/update the tool function in `tools/<category>.py`
3. Register it in `server.py` with `mcp.tool(your_function)`
4. Write tests in `tests/test_<category>.py`

## Questions?

Open an issue or email destek@yaparai.com

