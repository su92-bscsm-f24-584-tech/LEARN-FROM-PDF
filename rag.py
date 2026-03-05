from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
import os
CHROMA_DB_DIR = "chroma_db"

def get_embeddings():
    return HuggingFaceEmbeddings(
        model_name="all-MiniLM-L6-v2"
    )

def build_vectorstore(pdf_path):
    loader = PyPDFLoader(pdf_path)
    documents = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=700, chunk_overlap=100)
    chunks = text_splitter.split_documents(documents)
    if not chunks:
        raise ValueError("No text chunks found in PDF!")
    embeddings=get_embeddings()
    vectorstore = Chroma.from_documents(
        documents=chunks, 
        embedding=embeddings,
        persist_directory=CHROMA_DB_DIR
    ) 
    print(f"Vectorstore saved to {CHROMA_DB_DIR}")
    return vectorstore
def load_vectorstore(pdf_file):
    """Load an already saved Chroma vectorstore from disk."""
    embeddings=get_embeddings()
    vectorstore = Chroma(
        persist_directory=CHROMA_DB_DIR,
        embedding_function=embeddings
    )
    return vectorstore
def ask_offline_pdf(vectorstore,question):
    """Query the saved vectorstore for a question."""
    results = vectorstore.similarity_search(question, k=3)
    answer_text = ""
    sources = []
    print(f"\n--- Question: {question} ---")
    
    for doc in results:
        page_num = doc.metadata.get('page', 'unknown')
        content = doc.page_content
        answer_text += content + "\n\n"
        sources.append({"page": page_num, "content": content})

    return answer_text.strip(), sources  
'''if __name__ == "__main__":
    pdf_file = "C:\\Users\\imato\\AppData\\Local\\Pub\\Cache\\hosted\\pub.dev\\analyzer-8.2.0\\CG-20250913-1.pdf" 
    user_query = input("Enter your query: ") # Use any phrase, even if not in PDF
    ask_offline_pdf(pdf_file, user_query)
'''