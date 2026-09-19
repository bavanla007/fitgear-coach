"""
RAG Retrieval tool for Culpeper's Complete Herbal corpus.
"""
import vertexai
from vertexai.preview import rag

CORPUS_NAME = "projects/1083993840257/locations/us-central1/ragCorpora/1901038012238659584"
PROJECT_ID = "qwiklabs-gcp-03-bec4fda9e582"
LOCATION = "us-central1"


def consult_herbal_rag_corpus(query: str) -> str:
    """
    Search Culpeper's Complete Herbal RAG corpus for information on herbs, plants, remedies, and fitness recovery preparations.

    Args:
        query: What to look up (herb, plant name, ailment, or preparation).

    Returns:
        Matched passages from the corpus or a message if none found.
    """
    try:
        vertexai.init(project=PROJECT_ID, location=LOCATION)
        resp = rag.retrieval_query(
            text=query,
            rag_resources=[rag.RagResource(rag_corpus=CORPUS_NAME)],
            rag_retrieval_config=rag.RagRetrievalConfig(top_k=5),
        )
        contexts = getattr(resp.contexts, "contexts", [])
        passages = [c.text.strip() for c in contexts if getattr(c, "text", "").strip()]
        return "\n\n---\n\n".join(passages) if passages else "No relevant passages found."
    except Exception as e:
        return f"RAG retrieval error: {str(e)}"
