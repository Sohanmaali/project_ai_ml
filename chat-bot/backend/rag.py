import chromadb
from chromadb.utils import embedding_functions

# Initialize ChromaDB
client = chromadb.PersistentClient(path="chroma_db")
collection = client.get_or_create_collection(
    name="portfolio",
    metadata={"hnsw:space": "cosine"}
)

embedder = embedding_functions.DefaultEmbeddingFunction()

# Load and split data
def load_and_embed(path="about_me.txt"):
    with open(path, "r", encoding="utf-8") as f:
        text = f.read()

    chunks = [text[i:i+800] for i in range(0, len(text), 800)]

    for i, chunk in enumerate(chunks):
        collection.add(
            ids=[f"chunk_{i}"],
            documents=[chunk],
            embeddings=embedder([chunk])
        )

def search(query):
    results = collection.query(
        query_texts=[query],
        n_results=5
    )
    return "\n\n".join(results["documents"][0])
