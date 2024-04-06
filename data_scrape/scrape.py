from lxml import html
import requests
import re
from flask import Flask, render_template, request, redirect, url_for, jsonify

app = Flask(__name__)

@app.route("/scrape", methods = ["GET"])
def scrape_data():
    link = request.args.get("link")

    page = requests.get(link)
    tree = html.fromstring(page.content)
    comments = tree.xpath('//*[contains(concat( " ", @class, " " ), concat( " ", "reply", " " ))]//*[contains(concat( " ", @class, " " ), concat( " ", "postMessage", " " ))]')
    
    pattern = re.compile(r'>>?\d+')
    text_contents = [re.sub(pattern, '', comment.text_content().strip()).replace('"', "'") for comment in comments]
    text_contents
    scraped_data = {"text_contents": text_contents}
    return scraped_data

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=7000)