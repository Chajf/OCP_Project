from transformers import pipeline
from flask import Flask, render_template, request, redirect, url_for, jsonify
import requests

sentiment_pipeline = pipeline("sentiment-analysis", cache_dir = "./model_files")

app = Flask(__name__)

@app.route("/check_model", methods = ["POST"])
def check_model():
    requests.post("http://api:5000/check_model", json={"status":"Model OK"})