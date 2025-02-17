from flask import Flask, request, jsonify
from flask_cors import CORS  # Import CORS to fix cross-origin issues
import google.generativeai as genai

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

        response = get_gemini_response(user_input)

        return jsonify(response)
    except Exception as e:
        return jsonify({"error": f"Internal server error: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(port=5000, debug=True)  # Make sure Flask is running on port 5000
