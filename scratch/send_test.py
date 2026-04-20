import urllib.request
import json
import uuid
import os

url = 'http://127.0.0.1:5000/predict'
boundary = uuid.uuid4().hex
headers = {'Content-Type': f'multipart/form-data; boundary={boundary}'}

# let's write a real file to bypass "Invalid image"
file_bytes = b''
try:
    with open('test_image.jpg', 'rb') as f:
        file_bytes = f.read()
except:
    file_bytes = b'fake'

body = f'--{boundary}\r\nContent-Disposition: form-data; name="image"; filename="test.jpg"\r\nContent-Type: image/jpeg\r\n\r\n'.encode() + file_bytes + f'\r\n--{boundary}--\r\n'.encode()

req = urllib.request.Request(url, data=body, headers=headers, method='POST')

try:
    with urllib.request.urlopen(req) as response:
        print('RESPONSE:', response.read().decode())
except Exception as e:
    print('ERROR:', e.read().decode() if hasattr(e, 'read') else str(e))
