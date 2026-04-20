from flask import Flask, request, jsonify
from utils import predict_emotion
from flask_cors import CORS

app = Flask(__name__)
CORS(app)   # ✅ ADD THIS LINE


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

    return {"emotion": emotion}
    print(request.files)

if __name__ == '__main__':
    app.run(debug=True)