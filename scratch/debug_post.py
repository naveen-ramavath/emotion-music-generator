import requests
import json

url = 'http://127.0.0.1:5000/predict'
files = {'image': ('test.jpg', b'fake image data', 'image/jpeg')}

try:
    response = requests.post(url, files=files)
    print("STATUS:", response.status_code)
    print("RESPONSE:", response.json())
except Exception as e:
    print("ERROR:", e)
