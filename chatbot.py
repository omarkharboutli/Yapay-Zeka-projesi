from flask import Flask, request, jsonify
from flask_cors import CORS  # Import CORS to fix cross-origin issues
import google.generativeai as genai
from langdetect import detect  # Language detection library

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Configure Gemini API Key (Replace with your valid API key)
GEMINI_API_KEY = "AIzaSyDwhyq-fPb-Mtld6Ko1nOoqgkdbLa9t9s4"
genai.configure(api_key=GEMINI_API_KEY)

def get_gemini_response(prompt):
    try:
        model = genai.GenerativeModel("gemini-pro")
        response = model.generate_content(prompt)
        return {"response": response.text}
    except Exception as e:
        return {"error": f"Failed to generate response: {str(e)}"}

@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json()
        user_input = data.get("message", "").strip()

        if not user_input:
            return jsonify({"error": "Message cannot be empty"}), 400

        # Detect the language of the user's input
        language = detect(user_input)

        # Map detected language to a valid speech synthesis language code
        language_codes = {
            "en": "en-US",  # English
            "tr": "tr-TR",  # Turkish
            "es": "es-ES",  # Spanish
            "fr": "fr-FR",  # French
            "de": "de-DE",  # German
            "zh": "zh-CN",  # Chinese
            "ja": "ja-JP",  # Japanese
            "ar": "ar-SA",  # Arabic (Saudi Arabia)
            # Add more languages as needed
        }
        # Use the primary language code from langdetect and default to English if not supported
        language_code = language_codes.get(language.split("-")[0], "en-US")

        # Get the response from Gemini
        response = get_gemini_response(user_input)

        # Add the detected language code to the response
        response["language"] = language_code

        return jsonify(response)
    except Exception as e:
        return jsonify({"error": f"Internal server error: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(port=5000, debug=True)  # Make sure Flask is running on port 5000
