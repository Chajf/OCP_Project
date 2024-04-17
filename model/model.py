from transformers import pipeline
from flask import Flask, render_template, request, redirect, url_for, jsonify
import requests

sentiment_pipeline = pipeline("sentiment-analysis")

app = Flask(__name__)

# @app.route("/check_model", methods = ["POST"])
# def check_model():
#     return {"status":"Model OK"}
#     #requests.post("http://api:5000/check_model", json={"status":"Model OK"})

@app.route("/check_model", methods = ["GET"])
def check_model():
    return {"status":"Model OK"}
    #requests.post("http://api:5000/check_model", json={"status":"Model OK"})

@app.route("/predict", methods=["POST"])
def predict():
    data = request.json.get("data")
    pred = sentiment_pipeline(data)
    return {"pred": pred}

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=6000)