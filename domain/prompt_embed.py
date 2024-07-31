from sentence_transformers import SentenceTransformer

model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')


def prompt_encode(text):
    embeddings = model.encode(text)
    return embeddings
