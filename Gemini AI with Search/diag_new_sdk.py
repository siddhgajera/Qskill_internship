import os
from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
client = genai.Client(api_key=api_key)

print("Checking models with modern SDK...")
models = client.models.list()
for m in models:
    print(f"Model ID: {m.name}")

def test_config(model_id, use_search=True):
    print(f"\nTesting {model_id} (Search: {use_search})")
    try:
        config = None
        if use_search:
            config = types.GenerateContentConfig(
                tools=[types.Tool(google_search_retrieval=types.GoogleSearchRetrieval())]
            )
        response = client.models.generate_content(
            model=model_id,
            contents="Say hello",
            config=config
        )
        print(f"  SUCCESS: {response.text[:50]}...")
    except Exception as e:
        print(f"  FAILED: {e}")

# Test variations
test_config("gemini-1.5-flash", use_search=False)
test_config("gemini-1.5-flash", use_search=True)
test_config("models/gemini-1.5-flash", use_search=True)
test_config("gemini-2.0-flash-exp", use_search=True)
