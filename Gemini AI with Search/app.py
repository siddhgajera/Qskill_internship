import os
from google import genai
from google.genai import types
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure the Gemini API
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    print("Error: GOOGLE_API_KEY not found in .env file.")
    exit(1)

client = genai.Client(api_key=api_key)

def chat_with_gemini():
    print("--- Gemini AI with Search Grounding (Robust Mode) ---")
    print("Type 'exit' or 'quit' to end the conversation.")
    print("-----------------------------------------------------")

    # Start history
    history = []

    while True:
        user_input = input("You: ")
        
        if user_input.lower() in ['exit', 'quit']:
            break

        try:
            # Prepare contents
            contents = history + [types.Content(role='user', parts=[types.Part.from_text(text=user_input)])]
            
            try:
                # Attempt 1: With Search Tool (Gemini 2.0 Flash)
                response = client.models.generate_content(
                    model='gemini-2.0-flash',
                    contents=contents,
                    config=types.GenerateContentConfig(
                        tools=[types.Tool(google_search_retrieval=types.GoogleSearchRetrieval())]
                    )
                )
            except Exception:
                # Fallback: Simple Chat (Search tool not yet active/quota reached)
                response = client.models.generate_content(
                    model='gemini-2.0-flash',
                    contents=contents
                )
            
            # Print response
            print(f"\nGemini: {response.text}\n")
            
            # Update history
            history.append(types.Content(role='user', parts=[types.Part.from_text(text=user_input)]))
            history.append(types.Content(role='model', parts=[types.Part.from_text(text=response.text)]))
            
        except Exception as e:
            if "429" in str(e):
                print("\n[Quota Error] You've reached the limit. Please wait a moment.\n")
            else:
                print(f"An error occurred: {e}")

if __name__ == "__main__":
    chat_with_gemini()
