import os
import time
from monsterapi import client
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

api_key = os.getenv("MONSTER_API_KEY")
if not api_key:
    print("Error: MONSTER_API_KEY not found in .env file.")
    exit(1)

# Initialize MonsterAPI client
monster_client = client(api_key)

def process_pipeline(audio_file_path):
    print(f"--- Processing {audio_file_path} ---")

    # Step 1: Speech to Text (Whisper)
    print("1. Transcribing audio (Whisper-large-v3)...")
    try:
        # Note: monsterapi sdk usage might vary slightly, checking common pattern
        # The SDK usually takes model name and input data
        
        # Uploading file is often handled by the SDK specific call or we pass the path if supported
        # For simplicity in this demo, we assume the SDK handles path upload or we might need a direct request
        # Let's try the standard SDK call structure
        
        stt_result = monster_client.get_response(
            model='whisper-large-v3',
            data={
                "file": audio_file_path,
                # "server_url": "optional_callback" 
            }
        )
        
        # Check output structure (usually contains 'text')
        # The response structure depends on the specific model, verify this logic!
        if 'text' in stt_result:
            transcription = stt_result['text']
        elif 'output' in stt_result and 'text' in stt_result['output']:
             transcription = stt_result['output']['text']
        else:
            # Fallback for debugging
            transcription = str(stt_result)
            
        print(f"   Transcription: \"{transcription}\"")
        
    except Exception as e:
        print(f"STT Failed: {e}")
        return

    # Step 2: Text to Image (SDXL)
    print(f"\n2. Generating Image from text: \"{transcription}\"")
    try:
        tti_result = monster_client.get_response(
            model='sdxl-base-1.0',
            data={
                "prompt": transcription,
                "samples": 1,
                "steps": 30
            }
        )
        
        # Extract image URL
        # Usually result['output'] is a list of image URLs
        image_url = None
        if 'output' in tti_result:
            if isinstance(tti_result['output'], list):
                image_url = tti_result['output'][0]
            else:
                image_url = tti_result['output']
        
        if image_url:
            print(f"   Image Generated: {image_url}")
            print("   (Please open the URL to view and save the image)")
        else:
            print(f"   Image Generation response unclear: {tti_result}")

    except Exception as e:
        print(f"TTI Failed: {e}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        audio_path = sys.argv[1]
    else:
        # Default for testing
        audio_path = input("Enter path to audio file: ")
    
    if os.path.exists(audio_path):
        process_pipeline(audio_path)
    else:
        print("File not found.")
