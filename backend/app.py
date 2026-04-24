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
        # Find the links.txt file inside the correct emotion folder
        links_file = os.path.join(MUSIC_DIR, emotion.lower(), "links.txt")
        
        if os.path.exists(links_file):
            with open(links_file, "r") as f:
                # Read lines, strip whitespace, and filter out empty lines
                links = [line.strip() for line in f.readlines() if line.strip()]
            
            if links:
                # Get up to 10 links
                videos = links[:10]

    print("DEBUG Returning videos:", videos)
    
    return jsonify({
        "emotion": emotion,
        "videos": videos
    })

if __name__ == '__main__':
    app.run(debug=True)