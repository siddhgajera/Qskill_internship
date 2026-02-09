# Sentiment Analysis Web App

A Flask-based web application that performs sentiment analysis on text input and provides an interactive chatbot interface powered by Google Gemini.

## Features
- **Sentiment Analysis**: Analyze text using `TextBlob` to determine polarity (Positive, Negative, Neutral) and subjectivity.
- **Interactive Chat**: Chat with Gemini 2.0 Flash directly from the web interface.
- **Visual Feedback**: Dynamic display of sentiment scores.
- **Session Management**: Maintains chat history for context.

## Prerequisites
- Python 3.x
- Google Gemini API Key

## Installation
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Create a `.env` file and add your API key:
   ```
   GOOGLE_API_KEY=your_api_key_here
   ```

## Usage
Run the Flask application:
```bash
python app.py
```
Open your browser and navigate to `http://127.0.0.1:5000/`.

Enter text in the analysis box to see sentiment results or use the chat interface to interact with the AI.
