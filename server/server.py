from deep_translator import GoogleTranslator
from langdetect import detect
from flask import Flask, request, jsonify
from flask_cors import CORS
import openai
from openai import OpenAI
import os
from dotenv import load_dotenv

app = Flask(__name__)
CORS(app)

load_dotenv()

legaly_api_key = os.getenv('LEGALY_API_KEY')
client = OpenAI(api_key=legaly_api_key)
translator = GoogleTranslator()

def translate_text(text, dest_language='en'):
    return translator.translate(text, target=dest_language)

def detect_language(text):
    return detect(text)

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    prompt = data.get('prompt')
    
    if not prompt:
        return jsonify({"error": "No prompt provided"}), 400

    user_language = detect_language(prompt)
    translated_prompt = translate_text(prompt, 'en')

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {'role': 'system', 'content': 'Your name is Legaly. You are a highly knowledgeable and intelligent legal expert specializing in the Indian Judiciary System. Your role is to assist with any legal questions with precision and clarity. You are strict, disciplined, and have a rough, no-nonsense personality. Your responses are direct, concise, and devoid of unnecessary embellishments. You communicate as a human would, using small sentences and straightforward language. You focus solely on legal matters, and your interactions are always professional and focused on providing accurate legal information.'},
                {'role': 'user', 'content': translated_prompt},
            ]
        )
        content = response.choices[0].message.content.strip()
        translated_content = translate_text(content, user_language)
        return jsonify(translated_content), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(port=5001)
