import os
from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Configure Gemini API
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY environment variable is not set")
genai.configure(api_key=GEMINI_API_KEY)

# Function to get a free model that supports generateContent
def get_available_model():
    try:
        models = genai.list_models()
        # Prioritize officially supported models for generateContent
        supported_models = [
            'models/gemini-2.5-flash',
            'models/gemini-2.5-flash-lite',
            'models/gemini-2.5-pro',
            'models/gemini-2.0-flash',
            'models/gemini-2.0-flash-lite'
        ]
        for model in models:
            if model.name in supported_models and 'generateContent' in model.supported_generation_methods:
                return model.name
        # Fallback to any model supporting generateContent
        for model in models:
            if 'generateContent' in model.supported_generation_methods:
                return model.name
        raise ValueError("No suitable model found that supports generateContent")
    except Exception as e:
        raise ValueError(f"Error listing models: {str(e)}")

# Initialize the model
model_name = get_available_model()
model = genai.GenerativeModel(model_name)
print(f"Using model: {model_name}")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message')
    if not user_message:
        return jsonify({'error': 'No message provided'}), 400
    
    try:
        response = model.generate_content(user_message)
        bot_reply = response.text
        return jsonify({'reply': bot_reply})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
