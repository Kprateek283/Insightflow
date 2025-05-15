import cohere
import numpy as np
from typing import List
from dotenv import load_dotenv
import os
from app.vectorstore.faiss_index import generate_question_embedding, search_faiss_by_document

load_dotenv()

# Initialize Cohere client
COHERE_API_KEY = os.getenv("COHERE_API_KEY")
cohere_client = cohere.Client(COHERE_API_KEY)  # Replace with your actual API key

# Function to generate a response using Cohere
async def generate_answer(query: str, document_id: str) -> str:
    """
    Get the answer from Cohere by performing semantic search on the document and using the retrieved context.
    """
    # Generate the query embedding using Cohere (or your chosen embedding model)
    query_embedding = await generate_question_embedding(query)
    
    # Perform semantic search with FAISS
    top_k = 5
    search_results = await search_faiss_by_document(document_id, query_embedding, top_k)

    if not search_results:
        return "Sorry, I couldn't find relevant information in the document."

    # Combine the text from the most relevant chunks
    relevant_texts = [result["text"] for result in search_results]

    # Create the context for Cohere to generate an answer
    context = "\n\n".join(relevant_texts)

    # Prepare the prompt with context and the query
    prompt = f"Given the following information:\n\n{context}\n\nAnswer the following question:\n\n{query}"

    try:
        # Use Cohere to generate an answer
        response = cohere_client.generate(
            model='command',  # You can change the model type, like `xlarge`, `medium`, etc.
            prompt=prompt,
            max_tokens=250,
            temperature=0.7,  # Adjust the temperature for creativity
            k=1,
            stop_sequences=["\n"]
        )

        # Extract and return the answer from Cohere response
        answer = response.generations[0].text.strip()
        return answer

    except Exception as e:
        # Handle errors (e.g., API issues, invalid response)
        print(f"Error generating answer: {e}")
        return "Sorry, there was an issue generating the answer. Please try again later."
