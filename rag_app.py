"""
Local RAG Application using FAISS + Ollama

Features
--------
- TXT & PDF support
- SentenceTransformer embeddings
- FAISS vector search
- Ollama (llama3.2)
- Embedding cache
- FAISS cache
"""
import time
import json
from pathlib import Path

import faiss
import numpy as np
import ollama
from pypdf import PdfReader
from sentence_transformers import SentenceTransformer

# -----------------------------
# Configuration
# -----------------------------

DOCUMENT_FOLDER = "documents"
MODEL_NAME = "tinyllama"

EMBEDDING_FILE = "embeddings.npy"
INDEX_FILE = "faiss_index.bin"
CHUNK_FILE = "chunks.json"

print("Loading embedding model...")
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")


# -----------------------------
# Load Documents
# -----------------------------

def load_documents(folder_path=DOCUMENT_FOLDER):

    documents = []

    folder = Path(folder_path)
    folder.mkdir(exist_ok=True)

    # TXT files
    for file in folder.glob("*.txt"):
        with open(file, "r", encoding="utf-8") as f:
            documents.append((file.name, f.read()))

    # PDF files
    for file in folder.glob("*.pdf"):

        reader = PdfReader(file)

        text = ""

        for page in reader.pages:
            page_text = page.extract_text()

            if page_text:
                text += page_text + "\n"

        documents.append((file.name, text))

    return documents


# -----------------------------
# Chunking
# -----------------------------

def split_into_chunks(text, chunk_size=400, overlap=80):

    words = text.split()

    chunks = []

    start = 0

    while start < len(words):

        end = start + chunk_size

        chunks.append(" ".join(words[start:end]))

        start += chunk_size - overlap

    return chunks


# -----------------------------
# Embeddings
# -----------------------------

def create_embedding(text):

    return embedding_model.encode(
        text,
        normalize_embeddings=True
    ).tolist()


# -----------------------------
# Build FAISS Index
# -----------------------------

def build_index(documents):

    chunks = []
    embeddings = []

    print("\nCreating embeddings...")

    for filename, content in documents:

        text_chunks = split_into_chunks(content)

        for chunk in text_chunks:

            if not chunk.strip():
                continue

            vector = create_embedding(chunk)

            chunks.append((filename, chunk))
            embeddings.append(vector)

    if len(embeddings) == 0:
        raise Exception("No text found inside documents.")

    embeddings = np.array(embeddings).astype("float32")

    np.save(EMBEDDING_FILE, embeddings)

    with open(CHUNK_FILE, "w", encoding="utf-8") as f:
        json.dump(chunks, f, ensure_ascii=False, indent=2)

    index = faiss.IndexFlatIP(embeddings.shape[1])
    index.add(embeddings)

    faiss.write_index(index, INDEX_FILE)

    print("Embeddings saved.")
    print("FAISS index saved.")
    print(f"Indexed {len(chunks)} chunks.")

    return chunks, index


# -----------------------------
# Load Cached Index
# -----------------------------

def load_cached_index():

    if not (
        Path(EMBEDDING_FILE).exists()
        and Path(INDEX_FILE).exists()
        and Path(CHUNK_FILE).exists()
    ):
        return None, None

    print("\nLoading cached index...")

    index = faiss.read_index(INDEX_FILE)

    with open(CHUNK_FILE, "r", encoding="utf-8") as f:
        chunks = json.load(f)

    return chunks, index
# -----------------------------
# Retrieve Relevant Chunks
# -----------------------------

def find_relevant_chunks(question, chunks, index, top_k=6):

    question_embedding = np.array(
        embedding_model.encode(
            [question],
            normalize_embeddings=True
        ),
    dtype="float32"
    )

    distances, indices = index.search(question_embedding, top_k)

    retrieved = []

    for distance, idx in zip(distances[0], indices[0]):

        if idx == -1:
            continue

        filename, chunk = chunks[idx]

        retrieved.append((filename, chunk, distance))

    return retrieved


# -----------------------------
# Generate Answer
# -----------------------------

def generate_answer(question, context_chunks):

    context = "\n\n".join(context_chunks)

    prompt = f"""
You are a Retrieval-Augmented Generation assistant.

Answer ONLY from the supplied context.

Rules:

- Do not use prior knowledge.
- Do not guess.
- If the answer is missing, reply exactly:

I don't have enough information in the provided documents.

Give short and accurate answers.

Context:
{context}

Question:
{question}

Answer:
"""

    print("Generating answer...\n")

    try:

        response = ollama.chat(
            model=MODEL_NAME,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        return response.message.content

    except Exception as e:

        return f"Error communicating with Ollama:\n{e}"


# -----------------------------
# Main Program
# -----------------------------

def main():

    print("=" * 60)
    print("LOCAL RAG APPLICATION")
    print("=" * 60)

    print("\nLoading documents...")

    documents = load_documents()

    if not documents:
        print("\nNo TXT or PDF files found.")
        print("Add documents to the 'documents' folder.")
        return

    print(f"\nFound {len(documents)} document(s):")

    for filename, content in documents:
        print(f"✔ {filename} ({len(content)} characters)")

    # Try loading cached index
    chunks, index = load_cached_index()

    if chunks is None:

        chunks, index = build_index(documents)

    else:

        print(f"Loaded {len(chunks)} cached chunks.")
        print(f"FAISS vectors : {index.ntotal}")

    print("\nReady!")
    print("Type 'quit' to exit.\n")

    while True:

        question = input("Your question: ").strip()

        if question.lower() in ["quit", "exit", "q"]:

            print("\nGoodbye!")
            break

        if not question:
            continue

        print("\nSearching documents...")
        start = time.time()
        retrieved = find_relevant_chunks(
            question,
            chunks,
            index,
            top_k=3
        )

        if len(retrieved) == 0:

            print("\nNo relevant information found.\n")
            continue

        context_chunks = []

        for filename, chunk, distance in retrieved:

            context_chunks.append(chunk)

        answer = generate_answer(question, context_chunks)

        elapsed = time.time() - start

        print("=" * 60)
        print("FINAL ANSWER")
        print("=" * 60)
        print(answer)
        print("=" * 60)
        print(f"Response Time : {elapsed:.2f} seconds")
        print()


if __name__ == "__main__":
    main()