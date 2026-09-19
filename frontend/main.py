"""Minimal FastAPI proxy for a deployed A2A agent (Agent Runtime, agents-cli 1.1.0+).

The browser talks ONLY to this proxy (same origin, no CORS, no GCP creds in the
browser). The proxy authenticates with Application Default Credentials and
forwards chat to the deployed agent over the A2A protocol, returning replies as
structured parts the chat UI knows how to show:

  * {"kind": "text", "text": ...}  -> a normal chat bubble
  * {"kind": "a2ui", "data": ...}  -> one A2UI message (beginRendering /
    surfaceUpdate); static/index.html renders these as a card.
"""

import json
import os
import uuid
from pathlib import Path

import google.auth
import google.auth.transport.requests
import httpx
from a2a.client import ClientConfig, create_client
from a2a.types import Message, Part, Role, SendMessageRequest
from a2a.utils.constants import (
    PROTOCOL_VERSION_1_0,
    VERSION_HEADER,
    TransportProtocol,
)
from google.protobuf.json_format import MessageToDict
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles

RESOURCE = os.environ.get(
    "AGENT_ENGINE_RESOURCE_NAME",
    "projects/1083993840257/locations/us-central1/reasoningEngines/7291190907515174912",
)
# The agent's app directory (matches agent_directory in agents-cli-manifest.yaml).
AGENT_DIRECTORY = os.environ.get("AGENT_DIRECTORY", "app")
LOCATION = RESOURCE.split("/locations/")[1].split("/")[0]

A2A_BASE = (
    f"https://{LOCATION}-aiplatform.googleapis.com/reasoningEngines/v1/"
    f"{RESOURCE}/api/a2a/{AGENT_DIRECTORY}"
)

# Credentials lazily loaded on first request
_creds = None


def _get_creds():
    global _creds
    if _creds is None:
        _creds, _ = google.auth.default(
            scopes=["https://www.googleapis.com/auth/cloud-platform"]
        )
    return _creds


def _auth_headers() -> dict[str, str]:
    creds = _get_creds()
    creds.refresh(google.auth.transport.requests.Request())
    return {
        "Authorization": f"Bearer {creds.token}",
        "Content-Type": "application/json",
        VERSION_HEADER: PROTOCOL_VERSION_1_0,
    }


app = FastAPI()


@app.exception_handler(Exception)
async def _json_errors(request: Request, exc: Exception):
    return JSONResponse(
        status_code=200,
        content={
            "parts": [{"kind": "text", "text": f"Error: {type(exc).__name__}: {exc}"}]
        },
    )


# Reuse ONE A2A context per user so the agent remembers the conversation.
_contexts: dict[str, str] = {}


def _extract_a2a_parts(parts_list) -> list[dict]:
    out: list[dict] = []
    for p in parts_list:
        text = getattr(p, "text", None)
        if text:
            out.append({"kind": "text", "text": text})
            continue

        if hasattr(p, "HasField") and p.HasField("data"):
            data_dict = MessageToDict(p.data)
            # A2UI parts carry {"metadata": {...}, "data": {beginRendering/surfaceUpdate: ...}}
            payload = data_dict.get("data", data_dict) if isinstance(data_dict, dict) else data_dict
            out.append({"kind": "a2ui", "data": payload})
            continue

        url = getattr(p, "url", None)
        if url:
            out.append({"kind": "text", "text": f"[file: {url}]"})
            continue

        raw = getattr(p, "raw", None)
        if raw:
            mime = getattr(p, "media_type", "application/octet-stream")
            out.append({"kind": "text", "text": f"[binary content: {len(raw)} bytes, {mime}]"})
    return out


@app.post("/chat")
async def chat(req: Request):
    body = await req.json()
    message = body.get("message", "")
    user_id = body.get("user_id") or "web-user"
    parts: list[dict] = []

    context_id = _contexts.get(user_id, "")

    async with httpx.AsyncClient(headers=_auth_headers(), timeout=120) as http_client:
        config = ClientConfig(
            httpx_client=http_client,
            supported_protocol_bindings=[
                TransportProtocol.JSONRPC,
                TransportProtocol.HTTP_JSON,
            ],
        )
        a2a_client = await create_client(A2A_BASE, config)

        msg = Message(
            message_id=str(uuid.uuid4()),
            context_id=context_id,
            role=Role.ROLE_USER,
            parts=[Part(text=message)],
        )

        async for chunk in a2a_client.send_message(SendMessageRequest(message=msg)):
            if chunk.HasField("artifact_update"):
                if chunk.artifact_update.context_id:
                    _contexts[user_id] = chunk.artifact_update.context_id
                parts.extend(_extract_a2a_parts(chunk.artifact_update.artifact.parts))
            elif chunk.HasField("task"):
                if chunk.task.context_id:
                    _contexts[user_id] = chunk.task.context_id
                for artifact in chunk.task.artifacts:
                    parts.extend(_extract_a2a_parts(artifact.parts))
            elif chunk.HasField("message"):
                if chunk.message.context_id:
                    _contexts[user_id] = chunk.message.context_id
                parts.extend(_extract_a2a_parts(chunk.message.parts))

    if not parts:
        parts = [{"kind": "text", "text": "(The agent didn't return a reply.)"}]
    return JSONResponse({"parts": parts})


# Mount static directory relative to this main.py file
static_dir = Path(__file__).parent / "static"
app.mount("/", StaticFiles(directory=str(static_dir), html=True), name="static")


if __name__ == "__main__":
    import uvicorn

    port = int(os.environ.get("PORT", 8080))
    uvicorn.run(app, host="0.0.0.0", port=port)
