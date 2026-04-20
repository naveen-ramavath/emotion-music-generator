import numpy as np
import cv2
from tensorflow.keras.models import load_model
import os

# Load the newly trained model from the root directory instead of the old weights
model_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'emotion_model.h5'))
model = load_model(model_path)

# Ensure classes are in EXACT alphabetical order to match Keras flow_from_directory
emotions = ["angry", "disgust", "fear", "happy", "neutral", "sad", "surprise"]

# load OpenCV face cascade
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# preprocess image
def preprocess_image(image_bytes):
    nparr = np.frombuffer(image_bytes, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_GRAYSCALE)

    # handle error if image not read
    if img is None:
        return None

    # Detect faces
    faces = face_cascade.detectMultiScale(img, scaleFactor=1.3, minNeighbors=5)

    if len(faces) > 0:
        # Get largest face
        faces = sorted(faces, key=lambda x: x[2] * x[3], reverse=True)
        x, y, w, h = faces[0]
        # Crop to the face
        img = img[y:y+h, x:x+w]
    else:
        print("Warning: No face detected in the image.")

    img = cv2.resize(img, (48, 48))
    img = img / 255.0
    img = np.reshape(img, (1, 48, 48, 1))

    return img

# prediction function
def predict_emotion(image_bytes):
    img = preprocess_image(image_bytes)

    if img is None:
        return "Invalid image"

    preds = model.predict(img)
    print(f"Prediction Array: {preds[0]}")
    return emotions[np.argmax(preds)]