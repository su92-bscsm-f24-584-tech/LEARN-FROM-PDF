

````markdown
# 📚 PDF Learner - Offline PDF ChatBot

[![Python](https://img.shields.io/badge/Python-3.10-blue)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-2.3.2-orange)](https://flask.palletsprojects.com/)
[![Chroma](https://img.shields.io/badge/Vectorstore-Chroma-green)](https://www.trychroma.com/)

A **Flask-based PDF ChatBot** with **offline RAG (Retrieval-Augmented Generation)**.  
Upload PDFs, ask questions, and get **answers with sources**, powered by **Chroma vectorstore** and **LLaMA 3 Mini**.

---

## ✨ Features

- ✅ Upload PDFs and extract text into a vectorstore  
- ✅ Offline chat with embeddings & LLaMA model  
- ✅ Shows **relevant sources** in a toggleable panel  
- ✅ Reuses vectorstore for unchanged PDFs  
- ✅ Chat disabled until PDF upload  
- ✅ Prebuilt **LLaMA model + Python bindings** → no C++ compilation  
- ✅ Accessible on **LAN / same Wi-Fi**  

---

## 📂 Project Structure

```text
pdf-learner/
├─ app.py                     # Flask application
├─ rag.py                     # PDF processing & vectorstore
├─ gen.py                     # LLaMA chat & answer generation
├─ uploads/                   # Uploaded PDFs
├─ chroma_db/                 # Vectorstore database
├─ models/
│   └─ Phi-3-mini-4k-instruct-q4.gguf  # Prebuilt LLaMA model
├─ llama_cpp_python-0.3.2.dist-info    # Prebuilt llama_cpp bindings
├─ templates/
│   └─ index.html             # Chat UI + upload
├─ static/
│   └─ style.css              # Optional CSS
└─ README.md
````

> **Note:** Place `Phi-3-mini-4k-instruct-q4.gguf` in `models/`.
> Prebuilt `llama_cpp_python-0.3.2.dist-info` ensures **no compilation required**.

---

## 🛠️ Requirements

* Python 3.10
* CPU ≥ 2 cores (threads adjustable)
* Windows or Linux

Optional packages if not included:

```bash
pip install flask langchain_community langchain_huggingface langchain_chroma chromadb PyPDF2 numpy
```

---

## 🚀 Running the App

1️⃣ **Clone the repository**

```bash
git clone https://github.com/yourusername/pdf-learner.git
cd pdf-learner
```

2️⃣ **Run Flask**

```bash
python app.py
```

* Default host: all interfaces → accessible on LAN
* Default port: 5000 (changeable in `app.py`):

```python
app.run(host="0.0.0.0", port=5000, debug=True)
```

3️⃣ **Open in Browser**

* Local: [http://127.0.0.1:5000](http://127.0.0.1:5000)
* Another PC on same network: [http://<host-ip>:5000](http://<host-ip>:5000)

---

## 💬 Using the ChatBot

1. Click **`+` button** next to chat input → select PDF
2. Wait for **loading overlay**
3. Chat box is **enabled only after successful upload**
4. Type question → press **Send**
5. **Sources panel** appears with relevant pages
6. Toggle source panel using `<` button

---

## 🤖 LLaMA Model Integration

The chatbot uses **prebuilt LLaMA model** via `llama_cpp` to improve response:


> ⚡ **Adjust threads:** Change `n_threads` for your CPU to speed up inference.

---

## 🗂️ PDF Processing & Vectorstore

* Uploaded PDF saved in `uploads/`
* SHA256 hash → reuse vectorstore if PDF unchanged
* Rebuild vectorstore if PDF differs
* Uses **HuggingFace embeddings (`all-MiniLM-L6-v2`)**
* Supports **all text-based PDFs** (OCR needed for scanned PDFs)

---

## ⚠️ Troubleshooting

* **PermissionError on Windows:** Close `chroma_db/chroma.sqlite3` in other apps
* **Empty embeddings:** Ensure PDF is **text-based**
* **Cannot access LAN:** Check firewall and network

---

## 🧩 Optional Settings

* **Change port:** `app.run(host="0.0.0.0", port=<port>)`
* **Change threads:** `n_threads` in `gen.py`
* **Increase context tokens:** `n_ctx` in `gen.py`

---

## 💡 Tips for Users

* Place **LLaMA model** in:

```
pdf-learner/models/Phi-3-mini-4k-instruct-q4.gguf
```

* Include prebuilt Python bindings in project root:

```
llama_cpp_python-0.3.2.dist-info/
```

* Adjust **CPU threads** according to machine:

```python
llm = Llama(model_path=model_path, n_ctx=4096, n_threads=4, verbose=False)
```

