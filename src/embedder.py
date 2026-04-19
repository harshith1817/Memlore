from sentence_transformers import SentenceTransformer

model=SentenceTransformer('all-MiniLM-L6-v2')

def get_embedding(text: str):
    """
    Converts input text into embedding vector
    """
    embedding=model.encode(text, normalize_embeddings=True)
    return embedding