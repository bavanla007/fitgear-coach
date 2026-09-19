# FitGear Coach — Expert AI Fitness & Gear Advisor

FitGear Coach is an intelligent, multi-modal AI assistant powered by **Google ADK** (Agent Development Kit), **Gemini 2.5 Flash**, and **Vertex AI Agent Engine**. Designed for runners, triathletes, and outdoor fitness enthusiasts, FitGear Coach provides gear recommendations, route & weather guidance, race pacing calculations, workout plan management, multimodal gear visualizations, and herbal recovery knowledge.

---

## 🚀 Key Features & Capabilities

FitGear Coach implements the following fully integrated tools and Google Cloud services:

### 1. 🖼️ Multimodal Gear Visualization & Video Generation
- **Imagen 3 Image Generation**: Generates photorealistic product and gear visualizations using Vertex AI `imagen-3.0-generate-002`.
- **Gemini Omni Video Generation**: Produces short gear demo videos using Google's `gemini-omni-flash-preview` model via the Vertex AI Interactions API.
- **Google Cloud Storage (GCS)**: Automatically uploads generated media artifacts to a public GCS bucket (`fitgear-coach-assets-*`) and returns secure, public HTTPS media URLs.

### 2. 🗄️ Cloud Firestore Workout & Gear Catalog Management
- **Gear Catalog Search & Addition**: Searches and updates gear items stored in a Cloud Firestore collection (`fitgear-coach`).
- **Workout Plan Management**: Retrieves personalized intermediate and advanced training plans directly from Firestore.

### 3. 🗺️ Location & Environmental Intelligence
- **Google Maps Platform Integration**: Uses the **Geocoding API** for address resolution and the **Places API** (Text Search) to locate nearby running trails, parks, and fitness centers.
- **Live Weather Conditions**: Integrates with OpenWeatherMap API to evaluate outdoor running temperature, humidity, wind, and overall running safety.

### 4. 🌿 Vertex AI RAG Corpus (Complete Herbal Knowledge)
- **Herbal Recovery RAG**: Queries a dedicated Vertex AI Vector Search RAG Corpus (`ragCorpora`) containing *The Complete Herbal* text to provide natural recovery advice, herbal teas, and anti-inflammatory remedies.

### 5. ⏱️ Race Pacing & Code Execution
- **Race Split Calculator**: Computes target splits and pacing strategies for 5K, 10K, Half Marathon, and Full Marathon events.
- **Python Code Execution**: Uses `AgentEngineSandboxCodeExecutor` to safely execute Python code in Vertex AI Agent Engine for data processing.

### 6. 🧠 Memory Bank & Preference Persistence
- **ADK PreloadMemoryTool & Memory Callbacks**: Automatically persists user preferences (e.g., intermediate runner, wet terrain preference) across chat sessions using ADK Memory Bank.

### 7. 🎨 A2UI v0.8 Protocol Integration
- **Structured UI Components**: Renders rich, interactive UI cards (`Card`, `Column`, `Row`, `Text`, `Image`) directly in the chat frontend using the A2UI v0.8 schema specification.

---

## 📋 Status of Planned Features

| Feature | Implementation Status |
| :--- | :--- |
| Gemini 2.5 Flash Reasoning Agent | ✅ Implemented & Live |
| A2UI v0.8 Card Rendering | ✅ Implemented & Live |
| Imagen 3 Gear Image Generation | ✅ Implemented & Live |
| Gemini Omni Video Generation | ✅ Implemented & Live |
| Cloud Firestore Gear & Workouts | ✅ Implemented & Live |
| Google Maps Trails & Parks Search | ✅ Implemented & Live |
| OpenWeatherMap Running Weather | ✅ Implemented & Live |
| Vertex AI RAG Herbal Corpus | ✅ Implemented & Live |
| ADK Memory Bank Session Storage | ✅ Implemented & Live |
| Live Wearable / Bluetooth Sensor Sync | ⏳ *Planned, not yet implemented* |

---

## 🛠️ Architecture & Tech Stack

- **Agent Framework**: Google Agent Development Kit (ADK)
- **Primary LLM**: `gemini-2.5-flash`
- **Video Model**: `gemini-omni-flash-preview` (Global region)
- **Image Model**: `imagen-3.0-generate-002` (us-central1 region)
- **Hosting & Runtime**: Vertex AI Reasoning Engine / Agent Runtime & Google Cloud Run
- **Frontend**: FastHTML / FastAPI web interface with custom Emerald & Teal styling
- **Database**: Cloud Firestore
- **Vector Search**: Vertex AI RAG Engine
- **Media Storage**: Google Cloud Storage (GCS)

---

## 💻 Local Setup & Execution Guide

Follow these steps to run the FitGear Coach project locally on your machine.

### Prerequisites
- Python 3.11+
- [`uv`](https://github.com/astral-sh/uv) package manager installed
- Google Cloud SDK (`gcloud`) authenticated to your GCP Project with Vertex AI, Firestore, and Maps APIs enabled.

### 1. Environment Configuration

Export the required environment variables in your terminal:

```bash
export GOOGLE_CLOUD_PROJECT="<your-gcp-project-id>"
export GOOGLE_CLOUD_LOCATION="us-central1"
export GOOGLE_GENAI_USE_VERTEXAI="true"
export GOOGLE_MAPS_API_KEY="<your-google-maps-api-key>"
```

### 2. Install Dependencies

Install all dependencies in a local virtual environment:

```bash
uv sync
```

### 3. Run Unit & Integration Tests

Run the test suite to verify tool integration:

```bash
uv run pytest
```

### 4. Run the Agent Locally (ADK Playground)

Launch the ADK developer playground to inspect agent reasoning and tool calls:

```bash
uv run agents-cli playground
```

### 5. Launch the Frontend Web Server

Start the local web application:

```bash
PORT=8080 AGENT_ENGINE_RESOURCE_NAME="projects/<project-id>/locations/us-central1/reasoningEngines/<id>" AGENT_DIRECTORY="app" uv run python3 frontend/main.py
```

---

## 🚀 Deployment

To deploy the agent to Vertex AI Agent Runtime and the frontend to Cloud Run:

```bash
# Deploy Reasoning Engine Agent
uv run agents-cli deploy --project <your-gcp-project-id> --region us-central1 --deployment-target agent_runtime

# Deploy Frontend Web App to Cloud Run
gcloud run deploy fitgear-coach-frontend \
  --source frontend \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars AGENT_ENGINE_RESOURCE_NAME="projects/<project-id>/locations/us-central1/reasoningEngines/<id>",AGENT_DIRECTORY="app"
```
