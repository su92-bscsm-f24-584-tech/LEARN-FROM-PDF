import os
import rag as rag
from llama_cpp import Llama
def load_model():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    model = os.path.join(
        base_dir,
        "models",
        "Phi-3-mini-4k-instruct-q4.gguf"
    )
    llm = Llama(
        model_path = model,
        n_ctx=4096,
        n_threads=2,   # adjust to CPU cores
        verbose=False
    )
    return llm
   
def generate_answer(llm, context, question):
    prompt = f"""
You are an expert assistant.

Use the provided context to answer clearly.
Explain step-by-step in simple language.

Context:
{context}

Question:
{question}

Answer:
"""
    
    output = llm(
        prompt,
        max_tokens=500,
        temperature=0.3
    )

    return output["choices"][0]["text"]
def start(user_query,llm,vector):

    pdf_file = "C:\\Users\\imato\\AppData\\Local\\Pub\\Cache\\hosted\\pub.dev\\analyzer-8.2.0\\CG-20250913-1.pdf" 
    
    # if vector==" ":
    #    vector=rag.build_vectorstore(pdf_file)
    context,source=rag.ask_offline_pdf(vector, user_query)
    #     Load LLaMA model
   # llm = load_model()

    # Generate answer
    answer = generate_answer(llm, context, user_query)

    # Show answer
    #print("\nAnswer:\n", answer) 
    return answer,source
#if __name__ == "__main__":
 #   start()
    #user_query = input("Enter your query: ") # Use any phrase, even if not in PDF
   
#pass quiz1@CS