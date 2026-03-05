import rag as rag

def start():

    pdf_file = "C:\\Users\\imato\\AppData\\Local\\Pub\\Cache\\hosted\\pub.dev\\analyzer-8.2.0\\CG-20250913-1.pdf" 
    user_query = input("Enter your query: ") # Use any phrase, even if not in PDF
    
    vector=rag.load_vectorstore(pdf_file)
    context=rag.ask_offline_pdf(vector, user_query)
        # Load LLaMA model
  #  llm = load_model()

    # Generate answer
   # answer = generate_answer(llm, context, user_query)

    # Show answer
    #print("\nAnswer:\n", answer) 
if __name__ == "__main__":
    start()