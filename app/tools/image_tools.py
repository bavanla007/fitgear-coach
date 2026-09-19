"""
Image generation tool using gemini-3.1-flash-lite-image and Cloud Storage for FitGear Coach.
"""
import asyncio
import uuid
from google import genai
from google.genai import types
from google.cloud import storage
from google.adk.tools import ToolContext

BUCKET_NAME = "fitgear-coach-assets-qwiklabs-gcp-03-bec4fda9e582"
PROJECT_ID = "qwiklabs-gcp-03-bec4fda9e582"
MODEL_NAME = "gemini-3.1-flash-lite-image"


async def generate_gear_image(item_description: str, tool_context: ToolContext) -> str:
    """
    Generate a high-quality visualization image for fitness or running gear (e.g. shoes, watch, jacket, hydration vest).

    Args:
        item_description: Description of the gear item to visualize (e.g., 'lightweight trail running shoe in vivid neon blue').
        tool_context: ADK ToolContext injected automatically.

    Returns:
        The public HTTPS URL of the generated image uploaded to Cloud Storage.
    """
    try:
        # 1. Call gemini-3.1-flash-lite-image model in global region
        genai_client = genai.Client(
            project=PROJECT_ID,
            location="global",
            vertexai=True,
        )

        prompt = f"Professional studio photography of fitness gear: {item_description}, high resolution, detailed lighting."
        response = genai_client.models.generate_content(
            model=MODEL_NAME,
            contents=prompt,
        )

        if not response.candidates or not response.candidates[0].content.parts:
            return "Error: No image was returned by the generation model."

        part = response.candidates[0].content.parts[0]
        inline_data = getattr(part, "inline_data", None)
        if not inline_data:
            return "Error: Model response did not contain inline image data."

        image_bytes = inline_data.data
        mime_type = inline_data.mime_type or "image/jpeg"
        ext = "png" if "png" in mime_type else "jpg"

        filename = f"gear_{uuid.uuid4().hex[:8]}.{ext}"

        # 2. Save artifact in ToolContext for Playground Artifacts panel
        artifact_part = types.Part.from_bytes(data=image_bytes, mime_type=mime_type)
        res = tool_context.save_artifact(filename=filename, artifact=artifact_part)
        if asyncio.iscoroutine(res):
            await res

        # 3. Upload image bytes to public Cloud Storage bucket
        storage_client = storage.Client(project=PROJECT_ID)
        bucket = storage_client.bucket(BUCKET_NAME)
        object_key = f"generated_gear/{filename}"
        blob = bucket.blob(object_key)
        blob.upload_from_string(image_bytes, content_type=mime_type)

        public_url = f"https://storage.googleapis.com/{BUCKET_NAME}/{object_key}"
        return public_url
    except Exception as e:
        return f"Image generation failed: {str(e)}"
