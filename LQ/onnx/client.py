import requests
import numpy as np

np.random.seed(42)

request_data = np.random.uniform(0, 1, [1, 4]).tolist()
r = requests.post('http://127.0.0.1:8080/predict', 
json={'model': {'type': 'onnx', 'path': '/home/project/classifier.onnx'},
    'input': request_data})

print(r.json())

r = requests.post('http://127.0.0.1:8080/predict', 
json={'model': {'type': 'sklearn', 'path': '/home/project/regressor.pkl'},
    'input': request_data})

print(r.json())