import requests
import datetime
import schedule
import time
import threading

# PLACEHOLDERS - User should replace these with real API keys
OPENWEATHER_API_KEY = "your_openweather_api_key_here"
NEWS_API_KEY = "your_news_api_key_here"

def get_weather(city):
    """Fetches weather data using OpenWeatherMap API."""
    if OPENWEATHER_API_KEY == "your_openweather_api_key_here":
        return "Weather service is not configured. Please provide an API key."
    
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={OPENWEATHER_API_KEY}&units=metric"
    try:
        response = requests.get(url)
        data = response.json()
        if data["cod"] == 200:
            weather_desc = data["weather"][0]["description"]
            temp = data["main"]["temp"]
            return f"Current weather in {city} is {weather_desc} with a temperature of {temp} degrees Celsius."
        else:
            return f"Sorry, I couldn't find the weather for {city}."
    except Exception as e:
        return f"Error fetching weather: {str(e)}"

def get_news():
    """Fetches top news headlines using NewsAPI."""
    if NEWS_API_KEY == "your_news_api_key_here":
        return "News service is not configured. Please provide an API key."
    
    url = f"https://newsapi.org/v2/top-headlines?country=us&apiKey={NEWS_API_KEY}"
    try:
        response = requests.get(url)
        data = response.json()
        if data["status"] == "ok":
            articles = data["articles"][:5]
            headlines = [article["title"] for article in articles]
            return "Here are the top headlines: " + ". ".join(headlines)
        else:
            return "Sorry, I couldn't fetch the news at the moment."
    except Exception as e:
        return f"Error fetching news: {str(e)}"

def set_reminder(task, reminder_time_str, speech_engine):
    """Sets a reminder for a specific task at a given time."""
    try:
        # Validate HH:MM format
        time_parts = reminder_time_str.split(':')
        if len(time_parts) != 2:
            raise ValueError("Time must be in HH:MM format")
        
        hour = int(time_parts[0])
        minute = int(time_parts[1])
        if not (0 <= hour <= 23 and 0 <= minute <= 59):
            raise ValueError("Invalid hour or minute")

        def job():
            message = f"Reminder: {task}"
            print(f"\n[ALARM] {message}")
            # We don't use speech_engine directly here because it might 
            # not be thread-safe or we might need a fresh init in the thread
            # For now, let's keep it simple with print
            import pyttsx3
            local_engine = pyttsx3.init()
            local_engine.say(message)
            local_engine.runAndWait()

        schedule.every().day.at(reminder_time_str).do(job)
        return f"Okay, I've set a reminder for '{task}' at {reminder_time_str}."
    except Exception as e:
        return f"Failed to set reminder: {str(e)}. Please use HH:MM (24-hour) format."

def run_scheduler():
    """Thread function to run scheduled tasks."""
    while True:
        schedule.run_pending()
        time.sleep(10)

# Start scheduler thread
scheduler_thread = threading.Thread(target=run_scheduler, daemon=True)
scheduler_thread.start()
