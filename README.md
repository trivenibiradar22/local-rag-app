# 📚 Local RAG Application using FAISS + Ollama

A **Retrieval-Augmented Generation (RAG)** application that answers questions from your own **PDF** and **TXT** documents using **Sentence Transformers**, **FAISS**, and **Ollama**.

Unlike cloud-based solutions, this project runs completely **offline on your local machine**, ensuring your documents remain private while providing AI-powered question answering.

---

## 🚀 Features

- 📄 Supports **PDF** and **TXT** documents
- 🧠 Uses **Sentence Transformers (all-MiniLM-L6-v2)** for embeddings
- 🔍 Fast semantic search using **FAISS**
- 🤖 Local LLM using **Ollama**
- 💾 Automatic embedding caching
- ⚡ Automatic FAISS index caching
- 🔒 Fully offline after downloading the model
- 🐍 Simple Python implementation
- 📚 Retrieval-Augmented Generation (RAG)

---

## 🛠️ Technologies Used

- Python
- Ollama
- FAISS
- Sentence Transformers
- NumPy
- PyPDF

---

# 📂 Project Structure

```text
local-rag-app/
│
├── documents/
│   ├── sample.pdf
│   └── sample.txt
│
├── images/
│   └── demo.png
│
├── rag_app.py
├── requirements.txt
├── README.md
└── .gitignore
```

---

# ⚙️ Installation

## 1. Clone the Repository

```bash
git clone https://github.com/trivenibiradar22/local-rag-app.git

cd local-rag-app
```

---

## 2. Create a Virtual Environment

### Windows

```bash
python -m venv venv

venv\Scripts\activate
```

### Linux / macOS

```bash
python3 -m venv venv

source venv/bin/activate
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 4. Install Ollama

Download and install Ollama:

https://ollama.com/download

---

## 5. Download a Model

For lower RAM systems:

```bash
ollama pull tinyllama
```

For better response quality:

```bash
ollama pull llama3.2
```

---

# ▶️ Running the Application

Place your PDF or TXT files inside the **documents** folder.

Run:

```bash
python rag_app.py
```

---

# 💬 Example

```
Your question:
What is Arduino?
```

Output:

```
Arduino is an open-source microcontroller board used as the central controller in the Smart Dry and Wet Waste Segregation System.
```

---

# 📸 Demo

> Save a screenshot as **images/demo.png**.

```markdown
![Application Demo](images/demo.png)
```

When the image is uploaded, it will appear here:

![Application Demo](images/demo.png)

---

# 🧠 How It Works

1. Load PDF and TXT documents
2. Split documents into chunks
3. Generate embeddings using Sentence Transformers
4. Store embeddings in a FAISS index
5. Retrieve the most relevant chunks
6. Send the retrieved context to Ollama
7. Generate an answer using only the retrieved context

---

# 📦 Dependencies

- faiss-cpu
- sentence-transformers
- ollama
- numpy
- pypdf

Install all dependencies:

```bash
pip install -r requirements.txt
```

---

# 🔮 Future Improvements

- 🌐 Streamlit Web Interface
- 📁 Multiple document upload
- 📄 DOCX support
- 💬 Chat history
- 🧠 Conversation memory
- 📌 Source citations with page numbers
- ⚡ Incremental indexing
- 🔍 Hybrid Search (BM25 + FAISS)

---

# 👨‍💻 Author

**Triveni Biradar**

B.Tech Electronics & Telecommunication Engineering

MIT Academy of Engineering (MITAOE), Pune

GitHub: https://github.com/trivenibiradar22

---

# 🤝 Contributing

Contributions are welcome!

1. Fork the repository.
2. Create a new branch.
3. Commit your changes.
4. Open a Pull Request.

---

# ⭐ Support

If you found this project useful, please consider giving it a **⭐ Star** on GitHub.

It helps others discover the project and motivates future improvements.

---

## 📜 License

This project is licensed under the **MIT License**.