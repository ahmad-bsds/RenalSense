from sentence_transformers import SentenceTransformer

sentences = "This is an example sentence"

model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')


def encode(text):
    embeddings = model.encode(sentences)
    return embeddings


# f =encode(sentences)
# print(f)