import os
import random
from flask import Flask, request, jsonify, send_from_directory
from utils import predict_emotion
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# path to music folder
MUSIC_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'music'))

@app.route('/')
def home():
    return "Backend is running"

@app.route('/predict', methods=['POST'])
def predict():
    if 'image' not in request.files:
        return {"error": "No image uploaded"}, 400

    file = request.files['image']
    image = file.read()

    emotion = predict_emotion(image)

    songs = []

    if emotion and emotion not in ["Invalid image", "No face detected"]:
        emotion_dir = os.path.join(MUSIC_DIR, emotion.lower())
        print("DEBUG MUSIC_DIR:", MUSIC_DIR)
        print("DEBUG emotion_dir:", emotion_dir)
        print("DEBUG exists:", os.path.exists(emotion_dir))

        if os.path.exists(emotion_dir):
            try:
                songs = [
                    f for f in os.listdir(emotion_dir)
                    if f.endswith(".mp3")
                ]
                print("DEBUG songs count:", len(songs))
                # 🔥 optional: shuffle songs
                random.shuffle(songs)
            except Exception as e:
                print(f"Error reading music directory: {e}")

    print("DEBUG Returning songs:", songs)
    return jsonify({
        "emotion": emotion,
        "songs": songs
    })


@app.route('/music/<emotion>/<path:filename>')
def serve_music(emotion, filename):
    emotion_dir = os.path.join(MUSIC_DIR, emotion.lower())
    return send_from_directory(emotion_dir, filename)


if __name__ == '__main__':
    app.run(debug=True)