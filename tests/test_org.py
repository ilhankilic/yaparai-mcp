"""Tests for org ID resolver."""
import os
import pytest
from yaparai.tools._org import resolve_org_id


def test_resolve_from_param():
    assert resolve_org_id("explicit-org") == "explicit-org"


def test_resolve_from_env(monkeypatch):
    monkeypatch.setenv("YAPARAI_ORG_ID", "env-org-123")
    # Re-import to pick up env var (config is module-level)
    import importlib
    import yaparai.config as cfg
    import yaparai.tools._org as org_mod
    monkeypatch.setattr(org_mod, "YAPARAI_ORG_ID", "env-org-123")
    assert resolve_org_id() == "env-org-123"


def test_resolve_missing_raises():
    import yaparai.tools._org as org_mod
    original = org_mod.YAPARAI_ORG_ID
    org_mod.YAPARAI_ORG_ID = ""
    try:
        with pytest.raises(ValueError, match="Organization ID"):
            resolve_org_id(None)
    finally:
        org_mod.YAPARAI_ORG_ID = original
