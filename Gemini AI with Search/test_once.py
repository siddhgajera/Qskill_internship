import os
from google import genai
from google.genai import types
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")
client = genai.Client(api_key=api_key)

print("--- Testing Search Grounding ---")
try:
    response = client.models.generate_content(
        model='gemini-2.0-flash',
        contents="What is the price of Bitcoin right now?",
        config=types.GenerateContentConfig(
            tools=[types.Tool(google_search_retrieval=types.GoogleSearchRetrieval())]
        )
    )
    print(f"Gemini (Search): {response.text}")
except Exception as e:
    print(f"Search Failed: {e}")
    print("Trying Fallback (Basic Chat)...")
    try:
        response = client.models.generate_content(
            model='gemini-2.0-flash',
            contents="What is the price of Bitcoin right now?"
        )
        print(f"Gemini (Basic): {response.text}")
    except Exception as e2:
        print(f"Basic Chat also failed: {e2}")
