import asyncio
import base64
import uuid
from google import genai
from google.genai import types
from google.cloud import storage
from google.adk.tools import ToolContext

BUCKET_NAME = "fitgear-coach-assets-qwiklabs-gcp-03-bec4fda9e582"
PROJECT_ID = "qwiklabs-gcp-03-bec4fda9e582"


async def generate_gear_video(
    prompt: str,
    tool_context: ToolContext = None,
) -> str:
    """Generates a short video for an item in the fitgear domain using Google's Omni model (gemini-omni-flash-preview).

    Args:
        prompt: Description of the gear or fitness item to generate a video for.
        tool_context: Tool context for saving artifacts.

    Returns:
        Public GCS https URL pointing to the generated video file.
    """
    try:
        client = genai.Client(
            vertexai=True,
            project=PROJECT_ID,
            location="global",
        )

        interaction = client.interactions.create(
            model="gemini-omni-flash-preview",
            input=f"Generate a short video showing: {prompt}",
            response_format={"type": "VIDEO"},
        )

        video_bytes = None
        if hasattr(interaction, "output_video") and interaction.output_video:
            out = interaction.output_video
            if hasattr(out, "data") and out.data:
                video_bytes = out.data
            elif isinstance(out, dict) and out.get("data"):
                video_bytes = out["data"]

        if not video_bytes:
            return "Error: Failed to generate video bytes from gemini-omni-flash-preview."

        if isinstance(video_bytes, str):
            try:
                video_bytes = base64.b64decode(video_bytes)
            except Exception:
                video_bytes = video_bytes.encode("utf-8")

        filename = f"gear_video_{uuid.uuid4().hex[:8]}.mp4"

        # 1. Save artifact to Playground's Artifacts panel using types.Part
        if tool_context:
            artifact_part = types.Part.from_bytes(data=video_bytes, mime_type="video/mp4")
            res = tool_context.save_artifact(filename=filename, artifact=artifact_part)
            if asyncio.iscoroutine(res):
                await res

        # 2. Upload video bytes to public Cloud Storage bucket
        storage_client = storage.Client(project=PROJECT_ID)
        bucket = storage_client.bucket(BUCKET_NAME)
        blob = bucket.blob(filename)
        blob.upload_from_string(video_bytes, content_type="video/mp4")

        return f"https://storage.googleapis.com/{BUCKET_NAME}/{filename}"
    except Exception as e:
        return f"Video generation failed: {str(e)}"
