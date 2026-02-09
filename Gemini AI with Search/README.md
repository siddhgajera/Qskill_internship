# Gemini AI with Search Grounding

This project implements a console-based chat application using the Google Gemini API with Search Grounding enabled.

## Features
- Interactive chat interface in the terminal.
- Utilization of `gemini-2.0-flash` model.
- Integration with Google Search to provide grounded responses.
- Robust error handling for API quotas and connection issues.
- Session history retention for context-aware conversations.

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
Run the application:
```bash
python app.py
```
Type your query and press Enter. Type 'exit' or 'quit' to close.
