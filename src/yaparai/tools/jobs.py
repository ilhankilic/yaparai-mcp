"""Job status tracking tools."""

from __future__ import annotations

from yaparai.client import YaparAIClient


async def get_job_status(
    job_id: str,
) -> dict:
    """
    Check the status of a generation job.

    Use this to check on long-running jobs (especially video and music)
    or to retrieve the result URL of a completed job.
    No credits charged.

    Args:
        job_id: The job ID returned from a generate call

    Returns:
        Dict with job_id, status (pending/processing/succeeded/failed),
        mode, result_url (when done), error_message (if failed),
        and created_at timestamp.
    """
    client = YaparAIClient()
    return await client.get_job(job_id)
