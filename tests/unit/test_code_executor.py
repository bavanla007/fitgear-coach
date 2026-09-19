"""
Unit test for AgentEngineSandboxCodeExecutor initialization.
"""
from app.agent import root_agent
from google.adk.code_executors import AgentEngineSandboxCodeExecutor


def test_code_executor_configured():
    assert root_agent.code_executor is not None
    assert isinstance(root_agent.code_executor, AgentEngineSandboxCodeExecutor)
    assert root_agent.code_executor.agent_engine_resource_name == "projects/1083993840257/locations/us-central1/reasoningEngines/7291190907515174912"
