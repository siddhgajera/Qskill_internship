from flask import Flask, render_template, request, jsonify, session
from textblob import TextBlob
from google import genai
from google.genai import types
import os
from dotenv import load_dotenv

load_dotenv()

# Configure Gemini
api_key = os.getenv("GOOGLE_API_KEY")
client = None
if api_key:
    client = genai.Client(api_key=api_key)

app = Flask(__name__)
app.secret_key = os.urandom(24) # Needed for session

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    if request.method == 'POST':
        rawtext = request.form['rawtext']
        blob = TextBlob(rawtext)
        
        # Sentiment Analysis
        polarity = blob.sentiment.polarity
        subjectivity = blob.sentiment.subjectivity
        
        if polarity > 0:
            sentiment = "Positive"
            sentiment_class = "positive"
        elif polarity < 0:
            sentiment = "Negative"
            sentiment_class = "negative"
        else:
            sentiment = "Neutral"
            sentiment_class = "neutral"
            
        return render_template('index.html', 
                               sentiment=sentiment, 
                               sentiment_class=sentiment_class,
                               polarity=round(polarity, 2), 
                               subjectivity=round(subjectivity, 2), 
                               polarity_width=round((polarity + 1) * 50, 0),
                               subjectivity_width=round(subjectivity * 100, 0),
                               rawtext=rawtext)

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message')
    if not user_message:
        return jsonify({'error': 'No message provided'}), 400

    if not client:
        return jsonify({'error': 'Gemini API client not configured'}), 500

    try:
        # Initialize history in session if not present
        if 'chat_history' not in session:
            session['chat_history'] = []
            
        # Prepare contents with history
        contents = []
        for msg in session['chat_history'][-10:]: # Keep last 10 messages for context
            contents.append(types.Content(role=msg['role'], parts=[types.Part.from_text(text=msg['parts'][0])]))
        
        contents.append(types.Content(role='user', parts=[types.Part.from_text(text=user_message)]))

        try:
            # First attempt with Search Grounding
            response = client.models.generate_content(
                model='gemini-2.0-flash', # Using the model confirmed available on your key
                contents=contents,
                config=types.GenerateContentConfig(
                    tools=[types.Tool(google_search_retrieval=types.GoogleSearchRetrieval())]
                )
            )
        except Exception as tool_e:
            # Fallback to standard chat without tools if search causes errors (429/404)
            response = client.models.generate_content(
                model='gemini-2.0-flash',
                contents=contents
            )
        
        # Update history in session
        session['chat_history'].append({'role': 'user', 'parts': [user_message]})
        session['chat_history'].append({'role': 'model', 'parts': [response.text]})
        session.modified = True
        
        return jsonify({'response': response.text})
    except Exception as e:
        status_code = 500
        error_msg = str(e)
        if "429" in error_msg:
            status_code = 429
            error_msg = "Quota exceeded. Please try again in 30 seconds."
        return jsonify({'error': error_msg}), status_code

if __name__ == '__main__':
    app.run(debug=True)
