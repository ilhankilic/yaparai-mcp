"""Organization ID resolver — env var or explicit parameter."""

from yaparai.config import YAPARAI_ORG_ID


def resolve_org_id(org_id: str | None = None) -> str:
    """Return the org_id from parameter or YAPARAI_ORG_ID env var.

    Raises ValueError if neither is set.
    """
    oid = org_id or YAPARAI_ORG_ID
    if not oid:
        raise ValueError(
            "Organization ID is required. Either pass org_id parameter "
            "or set the YAPARAI_ORG_ID environment variable. "
            "Use list_organizations() to find your org ID."
        )
    return oid
