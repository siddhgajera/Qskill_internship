import os
from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
client = genai.Client(api_key=api_key)

models_to_test = [
    'models/gemini-2.0-flash-exp',
    'models/gemini-2.5-flash',
    'models/gemini-2.0-flash'
]

print("Testing Search Tool on specific models:")
for mid in models_to_test:
    print(f"Testing {mid}...", end=" ", flush=True)
    try:
        response = client.models.generate_content(
            model=mid,
            contents="What is the price of Bitcoin?",
            config=types.GenerateContentConfig(
                tools=[types.Tool(google_search_retrieval=types.GoogleSearchRetrieval())]
            )
        )
        print(f"SUCCESS: {response.text[:30]}...")
    except Exception as e:
        print(f"FAILED: {str(e)[:100]}")
