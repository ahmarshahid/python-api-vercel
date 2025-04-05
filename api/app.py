from flask import Flask, request, send_file
from flask_cors import CORS
from gtts import gTTS
import os
import tempfile

app = Flask(__name__)
CORS(app)  # Allow requests from Next.js or other frontends

@app.route('/generate-urdu-speech', methods=['POST'])
def generate_speech():
    try:
        data = request.get_json()
        text = data.get('text')
        language = data.get('language', 'ur')  # Default Urdu

        if not text:
            return {"error": "Text is required"}, 400
        
        if language not in ['ur', 'ar', 'en']:
            return {"error": "Unsupported language"}, 400

        # Use a temporary file for Vercel's serverless environment
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_audio:
            audio_file = temp_audio.name
            tts = gTTS(text=text, lang=language, slow=False)
            tts.save(audio_file)

            response = send_file(
                audio_file,
                mimetype="audio/mp3",
                as_attachment=True,
                download_name="speech.mp3"
            )

        # Clean up the temporary file after sending
        os.unlink(audio_file)
        return response

    except Exception as e:
        return {"error": str(e)}, 500

# Vercel requires this to work as a Serverless Function
def handler(request):
    return app(request.environ, request.start_response)