
import os 
import requests
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")


@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "name": "NEXUS",
        "version": "0.1 Experimental",
        "status": "online"
    })


@app.route("/api/health", methods=["GET"])
def health():
    return jsonify({
        "core": "ready",
        "gemini": bool(GEMINI_API_KEY)
    })


@app.route("/api/chat", methods=["POST"])
def chat():
    data = request.get_json(silent=True) or {}
    message = data.get("message", "").strip()

    if not message:
        return jsonify({"error": "Message manquant"}), 400

    if not GEMINI_API_KEY:
        return jsonify({
            "error": "La clé API Gemini n'est pas configurée."
        }), 503

    url = (
        "https://generativelanguage.googleapis.com/v1beta/"
        f"models/{GEMINI_MODEL}:generateContent"
    )

    payload = {
        "contents": [{
            "parts": [{"text": message}]
        }]
    }

    try:
        response = requests.post(
            url,
            params={"key": GEMINI_API_KEY},
            json=payload,
            timeout=45
        )
        response.raise_for_status()
        result = response.json()

        answer = result["candidates"][0]["content"]["parts"][0]["text"]

        return jsonify({
            "answer": answer,
            "engine": "Gemini",
            "nexus": "NEXUS CORE 0.1"
        })

    except requests.RequestException:
        return jsonify({
            "error": "Le service IA est momentanément indisponible."
        }), 502
    except (KeyError, IndexError, TypeError):
        return jsonify({
            "error": "Réponse IA inattendue."
        }), 502


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
