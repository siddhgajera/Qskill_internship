# Voice Activated Personal Assistant

A sophisticated Python-based desktop assistant capable of performing tasks via voice commands.

## Features
- **Voice Recognition**: Understands English commands using Google Speech Recognition.
- **Text-to-Speech**: Responds verbablly using Pyttsx3.
- **Task Scheduling**: Set reminders for specific times.
- **Real-Time Information**: Fetch current weather (OpenWeatherMap) and news headlines (NewsAPI).
- **Core Commands**:
  - Check weather/news.
  - Set reminders.
  - Quit/Exit.

## Prerequisites
- Python 3.x
- Microphone/Speakers
- API Keys: OpenWeatherMap, NewsAPI

## Installation
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
   (Note: You may need `PyAudio` which can have platform-specific installation requirements.)
   
2. Configure API Keys:
   Open `features.py` and replace the placeholder API keys:
   ```python
   OPENWEATHER_API_KEY = "your_actual_key"
   NEWS_API_KEY = "your_actual_key"
   ```

## Usage
Run the assistant:
```bash
python assistant.py
```
Wait for the prompt "Listening..." then speak your command clearly. Example: "What's the weather in New York?" or "Set a reminder for the meeting at 14:00".

Type 'exit' or say 'stop' to quit.
