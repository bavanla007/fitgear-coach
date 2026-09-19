"""
Unit tests for RAG tools.
"""
from app.tools.rag_tools import consult_herbal_rag_corpus


def test_consult_herbal_rag_corpus():
    res = consult_herbal_rag_corpus("mint for digestion")
    assert isinstance(res, str)
    assert len(res) > 0
