import os
from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
client = genai.Client(api_key=api_key)

models_to_test = [
    'models/gemini-1.5-flash',
    'models/gemini-1.5-flash-8b',
    'models/gemini-2.0-flash-exp',
    'models/gemini-2.0-flash'
]

print("Final testing with models/ prefix:")
for mid in models_to_test:
    try:
        response = client.models.generate_content(model=mid, contents="hi")
        print(f"  {mid}: SUCCESS")
    except Exception as e:
        print(f"  {mid}: FAILED - {str(e)[:100]}")
