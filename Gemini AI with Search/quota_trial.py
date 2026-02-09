import os
from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
client = genai.Client(api_key=api_key)

print("Starting Quota Trial...")

common_models = [
    'gemini-1.5-flash',
    'gemini-1.5-flash-8b',
    'gemini-1.5-pro',
    'gemini-2.0-flash-exp',
    'gemini-2.0-flash'
]

working_model = None

for model_id in common_models:
    print(f"\nTesting {model_id}:")
    try:
        # Try simple generation without search first
        response = client.models.generate_content(
            model=model_id,
            contents="hello"
        )
        print(f"  [Simple Connect] SUCCESS: {response.text[:20]}...")
        
        # Now try with search
        try:
            response_search = client.models.generate_content(
                model=model_id,
                contents="What time is it in Mumbai?",
                config=types.GenerateContentConfig(
                    tools=[types.Tool(google_search_retrieval=types.GoogleSearchRetrieval())]
                )
            )
            print(f"  [Search Tool] SUCCESS")
            working_model = model_id
            break # Found a fully working model!
        except Exception as e_search:
            print(f"  [Search Tool] FAILED: {str(e_search)[:100]}")
            
    except Exception as e_simple:
        print(f"  [Simple Connect] FAILED: {str(e_simple)[:100]}")

if working_model:
    print(f"\nBEST MODEL FOUND: {working_model}")
else:
    print("\nNo model found with active quota and search support.")
