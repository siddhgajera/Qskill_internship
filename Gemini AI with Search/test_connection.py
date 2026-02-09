import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=api_key)

def test_model(name, use_tools=False):
    print(f"\n--- Testing {name} (Tools: {use_tools}) ---")
    try:
        tools = [{'google_search_retrieval': {}}] if use_tools else None
        model = genai.GenerativeModel(model_name=name, tools=tools)
        response = model.generate_content("Hello! Give me a quick greeting.")
        print(f"Success: {response.text}")
        return True
    except Exception as e:
        print(f"Failed: {e}")
        return False

# Test common names
models_to_test = [
    'gemini-1.5-flash',
    'gemini-1.5-flash-latest',
    'gemini-1.5-pro',
    'gemini-2.0-flash-exp'
]

for name in models_to_test:
    # First test without tools
    if test_model(name, use_tools=False):
        # If model exists, test with search tools
        test_model(name, use_tools=True)
