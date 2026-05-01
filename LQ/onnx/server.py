from flask import Flask, request, jsonify
import numpy as np
import onnxruntime
import joblib
import threading

app = Flask(__name__)

class ONNXModelSingleton:
    _instances = {}
    _lock = threading.Lock()

    def __new__(cls, model_path: str):
        if model_path not in cls._instances:
            with cls._lock:
                if model_path not in cls._instances:
                    instance = super().__new__(cls)
                    instance.session = onnxruntime.InferenceSession(model_path)
                    cls._instances[model_path] = instance
        return cls._instances[model_path]

class SklearnModelSingleton:
    _instances = {}
    _lock = threading.Lock()

    def __new__(cls, model_path: str):
        if model_path not in cls._instances:
            with cls._lock:
                if model_path not in cls._instances:
                    instance = super().__new__(cls)
                    instance.model = joblib.load(model_path)
                    cls._instances[model_path] = instance
        return cls._instances[model_path]

@app.route("/predict", methods=["POST"])
def predict():
    info = request.get_json()
    model_type, model_path = info["model"]['type'], info["model"]['path']
    data = info["input"]
    if model_type == "onnx":
        model = ONNXModelSingleton(model_path)
        session = model.session
        input_name = session.get_inputs()[0].name
        outputs = session.run(None, {input_name: data})
        result = outputs[0].tolist()
    elif model_type == "sklearn":
        model = SklearnModelSingleton(model_path)
        result = model.model.predict(data).tolist()
    
    return jsonify({"data": result})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)