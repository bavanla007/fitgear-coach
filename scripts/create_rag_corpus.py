"""
Create serverless Vertex AI RAG Corpus and import text document.
"""
import vertexai
from vertexai.preview import rag
from vertexai.preview.rag.utils import resources as rr

PROJECT_ID = "qwiklabs-gcp-03-bec4fda9e582"
LOCATION = "us-central1"
GCS_PATH = "gs://fitgear-coach-assets-qwiklabs-gcp-03-bec4fda9e582/rag/pg49513.txt"


def create_corpus_and_import():
    vertexai.init(project=PROJECT_ID, location=LOCATION)

    print("Configuring Serverless mode for Vertex AI RAG Engine...")
    cfg = f"projects/{PROJECT_ID}/locations/{LOCATION}/ragEngineConfig"
    try:
        rag.update_rag_engine_config(
            rag_engine_config=rag.RagEngineConfig(
                name=cfg,
                rag_managed_db_config=rag.RagManagedDbConfig(mode=rr.Serverless()),
            )
        )
        print("Serverless RAG engine mode configured successfully.")
    except Exception as e:
        print(f"Engine config update note: {e}")

    print("Creating RAG Corpus with text-embedding-005...")
    corpus = rag.create_corpus(
        display_name="herbal-rag-corpus",
        embedding_model_config=rag.EmbeddingModelConfig(
            publisher_model="publishers/google/models/text-embedding-005"
        ),
    )
    print(f"CREATED_CORPUS_NAME: {corpus.name}")

    print(f"Importing and indexing {GCS_PATH} into corpus {corpus.name}...")
    resp = rag.import_files(
        corpus_name=corpus.name,
        paths=[GCS_PATH],
        transformation_config=rag.TransformationConfig(
            chunking_config=rag.ChunkingConfig(chunk_size=512, chunk_overlap=100)
        ),
    )
    print(f"Import completed! Imported files count: {resp.imported_rag_files_count}")
    return corpus.name


if __name__ == "__main__":
    create_corpus_and_import()
