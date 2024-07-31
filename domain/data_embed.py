from sentence_transformers import SentenceTransformer
from domain.document_chunks import chunk_text

sentences = chunk_text()

model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')


def encode(text):
    embeddings = model.encode(sentences)
    return embeddings
