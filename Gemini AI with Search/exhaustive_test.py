import os
from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
client = genai.Client(api_key=api_key)

print("Starting Exhaustive Model Test...")

models = client.models.list()
working_models = []

for m in models:
    name = m.name
    # Skip models that are obviously not for chat (embeddings, etc)
    if any(keyword in name.lower() for keyword in ['chat', 'gemini', 'learn']) and 'embedding' not in name.lower():
        print(f"Testing {name}...", end=" ", flush=True)
        try:
            response = client.models.generate_content(
                model=name,
                contents="hi"
            )
            print("SUCCESS")
            working_models.append(name)
        except Exception as e:
            err = str(e).split('.')[0] # Get short error
            print(f"FAILED ({err})")

print("\n--- Summary ---")
if working_models:
    print("Working models found:")
    for w in working_models:
        print(f" - {w}")
else:
    print("No working chat models found. Please check your API key billing/tier status.")

with open("working_models.txt", "w") as f:
    f.write("\n".join(working_models))
