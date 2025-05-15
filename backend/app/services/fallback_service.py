import os
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get the API key from environment variables
AI21_API_KEY = os.getenv('AI21_API_KEY')
if not AI21_API_KEY:
    raise ValueError("API key for AI21 Labs is missing. Set it in the .env file.")

# AI21 Labs API URL
AI21_URL = "https://api.ai21.com/studio/v1/jurassic-1/complete"

# Define the headers for the API request
HEADERS = {
    'Authorization': f'Bearer {AI21_API_KEY}',
    'Content-Type': 'application/json',
}

async def fallback_answer(question: str) -> str:
    """
    Use AI21 Labs Jurassic-1 model for answering questions when the context is not available.
    """
    # Prepare the data to send to the API
    data = {
        "prompt": question,
        "numResults": 1,  # We just want one result from the model
        "maxTokens": 100,  # Maximum number of tokens for the answer
        "temperature": 0.7,  # Control randomness of the model's output
    }

    try:
        # Send the request to the AI21 API
        response = requests.post(AI21_URL, headers=HEADERS, json=data)

        # Check if the response was successful
        if response.status_code == 200:
            result = response.json()
            # Extract the answer from the response
            answer = result['completions'][0]['text'].strip()
            return answer
        else:
            # Handle API errors
            raise Exception(f"AI21 API request failed with status code {response.status_code}: {response.text}")
    except Exception as e:
        raise Exception(f"Error in fetching fallback answer from AI21 Labs: {str(e)}")
