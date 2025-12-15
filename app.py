from flask import Flask, request, jsonify
from flask_cors import CORS
import anthropic
import os

app = Flask(__name__)
CORS(app)

client = anthropic.Anthropic(api_key=os.environ.get("CLAUDE_API_KEY"))

@app.route("/")
def home():
    return jsonify({"status": "MedAgram API running"})

@app.route("/hint", methods=["POST"])
def get_hint():
    try:
        data = request.json
        word = data.get("word", "")
        category = data.get("category", "")
        
        message = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=150,
            messages=[{
                "role": "user",
                "content": f'Give a funny, clever one-sentence hint for "{word}" (category: {category}). Do NOT say the word.'
            }]
        )
        return jsonify({"hint": message.content[0].text.strip()})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/iq-hint", methods=["POST"])
def get_iq_hint():
    try:
        data = request.json
        word = data.get("word", "")
        category = data.get("category", "")
        
        message = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=150,
            messages=[{
                "role": "user",
                "content": f'Create a cryptic, intellectual one-sentence hint using wordplay for "{word}" (category: {category}). Do NOT say the word.'
            }]
        )
        return jsonify({"hint": message.content[0].text.strip()})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/explain", methods=["POST"])
def explain_hint():
    try:
        data = request.json
        word = data.get("word", "")
        hint = data.get("hint", "")
        
        message = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=200,
            messages=[{
                "role": "user",
                "content": f'The answer was "{word}". The hint was: "{hint}". Briefly explain the wordplay in 1-2 sentences.'
            }]
        )
        return jsonify({"explanation": message.content[0].text.strip()})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
