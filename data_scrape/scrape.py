from lxml import html
import requests
import re
from flask import Flask, render_template, request, redirect, url_for, jsonify

app = Flask(__name__)

@app.route("/scrape")
def scrape_data():
    pass

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=7000)