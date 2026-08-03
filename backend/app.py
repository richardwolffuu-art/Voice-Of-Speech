"""
Utter — Open Source Text-to-Speech Backend
--------------------------------------------
100% free & open source stack:
  - espeak-ng  -> converts text to speech (WAV)  [GPL-3.0, no API key]
  - ffmpeg     -> converts WAV to MP3            [LGPL/GPL, no API key]
  - Flask      -> serves the API + the website

No paid API, no signup, no rate limits other than your own server's.
"""

import os
import subprocess
import tempfile
import uuid

from flask import Flask, request, send_file, jsonify, send_from_directory
from flask_cors import CORS

app = Flask(__name__, static_folder="static", static_url_path="")
CORS(app)  # allow requests from any origin (Vercel frontend, etc.)

# Voices we expose in the dropdown -> mapped to real espeak-ng voice codes
VOICES = {
    "en-us-male":    "en-us",
    "en-gb-male":    "en-gb",
    "en-scotland":   "en-gb-scotland",
    "hindi-male":    "hi",
    "hindi-mbrola-1": "mb/mb-in1",
    "hindi-mbrola-2": "mb/mb-in2",
    "spanish":       "es",
    "french":        "fr",
    "german":        "de",
    "arabic":        "ar",
}

OUTPUT_DIR = tempfile.mkdtemp(prefix="utter_tts_")


@app.route("/")
def home():
    return send_from_directory(app.static_folder, "index.html")


@app.route("/api/voices")
def list_voices():
    return jsonify(list(VOICES.keys()))


@app.route("/api/tts", methods=["POST"])
def tts():
    data = request.get_json(force=True)
    text = (data.get("text") or "").strip()
    voice_key = data.get("voice", "en-us-male")
    rate = int(data.get("rate", 175))     # words per minute, espeak default ~175
    pitch = int(data.get("pitch", 50))    # 0-99

    if not text:
        return jsonify({"error": "No text provided"}), 400
    if len(text) > 5000:
        return jsonify({"error": "Text too long (max 5000 characters)"}), 400

    voice_code = VOICES.get(voice_key, "en-us")
    job_id = uuid.uuid4().hex
    wav_path = os.path.join(OUTPUT_DIR, f"{job_id}.wav")
    mp3_path = os.path.join(OUTPUT_DIR, f"{job_id}.mp3")

    try:
        # Step 1: text -> wav using espeak-ng (open source engine, runs locally)
        subprocess.run(
            [
                "espeak-ng",
                "-v", voice_code,
                "-s", str(rate),
                "-p", str(pitch),
                "-w", wav_path,
                text,
            ],
            check=True,
            capture_output=True,
            timeout=30,
        )

        # Step 2: wav -> mp3 using ffmpeg (open source, real downloadable file)
        subprocess.run(
            ["ffmpeg", "-y", "-i", wav_path, "-codec:a", "libmp3lame", "-qscale:a", "2", mp3_path],
            check=True,
            capture_output=True,
            timeout=30,
        )
    except subprocess.CalledProcessError as e:
        return jsonify({"error": "TTS engine failed", "detail": e.stderr.decode(errors="ignore")}), 500
    finally:
        if os.path.exists(wav_path):
            os.remove(wav_path)

    return send_file(
        mp3_path,
        mimetype="audio/mpeg",
        as_attachment=False,
        download_name="utter-speech.mp3",
    )


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
