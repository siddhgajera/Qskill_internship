import speech_recognition as sr
import pyttsx3
import features
import sys

# Initialize the text-to-speech engine
engine = pyttsx3.init()

# Optional: Set properties for the voice
voices = engine.getProperty('voices')
if voices:
    engine.setProperty('voice', voices[0].id)  # Standard voice
engine.setProperty('rate', 150)  # Speed of speech

def speak(text):
    """Voice response from the assistant."""
    print(f"Assistant: {text}")
    try:
        engine.say(text)
        engine.runAndWait()
    except Exception as e:
        print(f"[Audio Output Error: {e}] (Text only mode active)")

def listen():
    """Listens for a voice command and converts it to text."""
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("\nListening...")
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source, duration=1)
        audio = r.listen(source)

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"User: {query}\n")
    except Exception as e:
        print("Could not understand. Please say that again.")
        return "None"
    return query.lower()

def get_input(prompt_text):
    """Gets input from voice or keyboard fallback."""
    try:
        query = listen()
        if query == "none":
            raise Exception("Voice recognizer returned none")
        return query
    except Exception as e:
        print(f"[{e}] Falling back to text input...")
        return input(f"{prompt_text} (Type here): ").lower()

def process_command(command):
    """Routes the command to the appropriate feature."""
    if 'weather' in command:
        speak("Which city?")
        city = get_input("Enter city name")
        weather_report = features.get_weather(city)
        speak(weather_report)

    elif 'news' in command:
        speak("Fetching headlines for you.")
        news_report = features.get_news()
        speak(news_report)

    elif 'reminder' in command or 'set a reminder' in command:
        speak("What should I remind you about?")
        task = get_input("Enter task description")
        
        speak("At what time? (Please use 24-hour format, e.g., 14:30)")
        reminder_time = get_input("Enter time (HH:MM)")
        
        # Simple cleaning of reminder_time if it's voice recognized
        reminder_time = reminder_time.replace(" ", "").replace(".", ":")
        
        reminder_status = features.set_reminder(task, reminder_time, engine)
        speak(reminder_status)

    elif 'stop' in command or 'exit' in command or 'quit' in command:
        speak("Goodbye!")
        sys.exit()

    else:
        speak("I'm not sure how to help with that yet. I can check the weather, read the news, or set a reminder.")

if __name__ == "__main__":
    speak("Hello! I am your personal assistant. How can I help you today?")
    
    while True:
        query = get_input("What can I do for you?")
        if query != "none":
            process_command(query)
