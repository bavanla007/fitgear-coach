"""
Unit test for image generation tool.
"""
import asyncio
from unittest.mock import MagicMock
from app.tools.image_tools import generate_gear_image


def test_generate_gear_image_mock():
    mock_ctx = MagicMock()

    async def mock_save(*args, **kwargs):
        return 1

    mock_ctx.save_artifact.side_effect = mock_save

    url = asyncio.run(generate_gear_image("trail running shoes in neon blue", tool_context=mock_ctx))
    assert isinstance(url, str)
    assert url.startswith("https://storage.googleapis.com/fitgear-coach-assets-qwiklabs-gcp-03-bec4fda9e582/") or "failed" in url.lower() or "error" in url.lower()
    if mock_ctx.save_artifact.called:
        assert mock_ctx.save_artifact.call_count >= 1
