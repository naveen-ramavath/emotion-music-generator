import urllib.request
import json
import uuid
import os
import cv2
import numpy as np

url = 'http://127.0.0.1:5000/predict'
boundary = uuid.uuid4().hex
headers = {'Content-Type': f'multipart/form-data; boundary={boundary}'}

# create valid simple image
img = np.zeros((480, 640, 3), dtype=np.uint8)
img[100:300, 100:300] = 255
_, img_encoded = cv2.imencode('.jpg', img)

file_bytes = img_encoded.tobytes()

body = f'--{boundary}\r\nContent-Disposition: form-data; name="image"; filename="test.jpg"\r\nContent-Type: image/jpeg\r\n\r\n'.encode() + file_bytes + f'\r\n--{boundary}--\r\n'.encode()

req = urllib.request.Request(url, data=body, headers=headers, method='POST')

try:
    with urllib.request.urlopen(req) as response:
        print('RESPONSE:', response.read().decode())
except Exception as e:
    print('ERROR:', e.read().decode() if hasattr(e, 'read') else str(e))
