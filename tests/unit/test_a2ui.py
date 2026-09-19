"""
Unit tests for A2UI schema manager and callback.
"""
from app.agent import root_agent
from app.a2ui_utils import a2ui_callback


def test_a2ui_configured():
    assert root_agent.after_model_callback == a2ui_callback
    assert "A2UI" in root_agent.instruction or "beginRendering" in root_agent.instruction
