import json
from pathlib import Path

import faiss
from sentence_transformers import SentenceTransformer


PROJECT_ROOT = Path(__file__).resolve().parents[2]
CHUNKS_FILE = (
    PROJECT_ROOT / "corpus" / "processed" / "regulation_chunks.json"
)
INDEX_FILE = PROJECT_ROOT / "corpus" / "processed" / "regulations.faiss"
METADATA_FILE = PROJECT_ROOT / "corpus" / "processed" / "regulation_metadata.json"

MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"


class RegulationSearch:
    def __init__(self):
        if not CHUNKS_FILE.exists():
            raise FileNotFoundError(
                f"Missing extracted regulation text: {CHUNKS_FILE}"
            )

        with CHUNKS_FILE.open("r", encoding="utf-8") as file:
            self.chunks = json.load(file)

        if not self.chunks:
            raise ValueError("No regulation chunks are available.")

        print("Loading embedding model...")
        self.model = SentenceTransformer(MODEL_NAME)

        texts = [chunk["text"] for chunk in self.chunks]

        print(f"Creating embeddings for {len(texts)} chunks...")
        embeddings = self.model.encode(
            texts,
            normalize_embeddings=True,
            convert_to_numpy=True,
        )

        embeddings = embeddings.astype("float32")

        self.index = faiss.IndexFlatIP(embeddings.shape[1])
        self.index.add(embeddings)

        # Save the index and its corresponding metadata.
        faiss.write_index(self.index, str(INDEX_FILE))

        with METADATA_FILE.open("w", encoding="utf-8") as file:
            json.dump(self.chunks, file, ensure_ascii=False, indent=2)

        print("Semantic search index created successfully.")

    def search(self, query: str, top_k: int = 3):
        if not query.strip():
            raise ValueError("Search query cannot be empty.")

        top_k = max(1, min(top_k, len(self.chunks)))

        query_embedding = self.model.encode(
            [query],
            normalize_embeddings=True,
            convert_to_numpy=True,
        ).astype("float32")

        scores, indices = self.index.search(query_embedding, top_k)

        results = []

        for score, idx in zip(scores[0], indices[0]):
            if idx < 0:
                continue

            chunk = self.chunks[int(idx)]

            results.append(
                {
                    "source": chunk["source"],
                    "page": chunk["page"],
                    "chunk_id": chunk["chunk_id"],
                    "text": chunk["text"],
                    "similarity": round(float(score), 4),
                }
            )

        return results


if __name__ == "__main__":
    searcher = RegulationSearch()

    question = (
        "What rules govern minimum attendance and "
        "condonation of attendance shortage?"
    )

    print(f"\nSearch query: {question}\n")

    for result in searcher.search(question, top_k=3):
        print("-" * 70)
        print(f"Source: {result['source']}")
        print(f"Page: {result['page']}")
        print(f"Similarity: {result['similarity']}")
        print(result["text"])
        print()

