from flask import Flask, render_template, request, jsonify
import os, hashlib,shutil
import rag as rag
import gen as gen

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
CHROMA_DB_DIR = "chroma_db"
HASH_FILE = os.path.join(CHROMA_DB_DIR, "pdf_hash.txt")
if not os.path.exists('uploads'):
    os.makedirs('uploads')

llm = None   # ✅ global variable
vectorstore=None

@app.route("/")
def home():
    return render_template("index.html")
'''

@app.route("/upload", methods=["POST"])
def upload_file():
    global llm
    if 'file' not in request.files:
        return jsonify({"error": "No file"}), 400

    file = request.files['file']
    if file.filename == "":
        return jsonify({"error": "Empty filename"}), 400

    filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(filepath)

    llm = gen.load_model()
    rag.build_vectorstore(filepath)

    return jsonify({"result": "File processed successfully ✅"})

'''
def get_pdf_hash(pdf_path):
    """Return SHA256 hash of PDF content."""
    sha = hashlib.sha256()
    with open(pdf_path, "rb") as f:
        while chunk := f.read(8192):
            sha.update(chunk)
    return sha.hexdigest()

@app.route("/upload", methods=["POST"])
def upload_file():
    global vectorstore
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files['file']
    if file.filename == "":
        return jsonify({"error": "Empty filename"}), 400

    filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(filepath)

    # Compute hash
    new_hash = get_pdf_hash(filepath)

    # Read old hash
    old_hash = None
    if os.path.exists(HASH_FILE):
        with open(HASH_FILE, "r") as f:
            old_hash = f.read().strip()

    if old_hash == new_hash:
        # Same PDF, reuse vectorstore
        vectorstore = rag.load_vectorstore()
        print("Loaded existing vectorstore (PDF unchanged).")
    else:
        # Different PDF → delete old DB
        if os.path.exists(CHROMA_DB_DIR):
            shutil.rmtree(CHROMA_DB_DIR)
        os.makedirs(CHROMA_DB_DIR, exist_ok=True)

        # Build new vectorstore
        vectorstore = rag.build_vectorstore(filepath)

        # Save new hash
        with open(HASH_FILE, "w") as f:
            f.write(new_hash)
        print("Built new vectorstore (PDF changed).")

    return jsonify({"message": "File uploaded successfully!"})
@app.route("/ask", methods=["POST"])
def ask():
    global llm
    data = request.json
    message = data["message"]

    if llm is None:
        return jsonify({"answer": "Upload a file first!", "sources":[]})

    response, sources = gen.start(message, llm, vectorstore)
    return jsonify({"answer": response, "sources": sources})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)