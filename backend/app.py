import os
import random
from flask import Flask, request, jsonify
from utils import predict_emotion
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

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

    videos = []
    if emotion and emotion not in ["Invalid image", "No face detected"]:
        # Read from youtube_links.txt from the root directory
        youtube_links_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'youtube_links.txt'))
        
        if os.path.exists(youtube_links_path):
            try:
                with open(youtube_links_path, "r", encoding="utf-8") as f:
                    content = f.read()
                    # Execute the file content to parse the python dictionary
                    local_vars = {}
                    exec(content, {}, local_vars)
                    youtube_links = local_vars.get("youtube_links", {})
                    
                    links = youtube_links.get(emotion.lower(), [])
                    if links:
                        # Get up to 10 links
                        videos = links[:10]
            except Exception as e:
                print("Error loading youtube_links.txt:", e)

    print("DEBUG Returning videos:", videos)
    
    return jsonify({
        "emotion": emotion,
        "videos": videos
    })

if __name__ == '__main__':
    app.run(debug=True)