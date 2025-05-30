import os
from flask import Flask, render_template, request
import requests

app = Flask(__name__)

# Set these to your Azure resource details
AZURE_ENDPOINT = "https://shreyassentimentanalysis.cognitiveservices.azure.com/"
AZURE_KEY = "2kCBlNjFnEGX6cbKyp9OwIAqwvgCT9SkXqAmRqLdGYBNDgawZIieJQQJ99BEACYeBjFXJ3w3AAAaACOGdxzr"

def analyze_sentiment(text):
    url = AZURE_ENDPOINT + "/text/analytics/v3.1/sentiment"
    headers = {
        "Ocp-Apim-Subscription-Key": AZURE_KEY,
        "Content-Type": "application/json"
    }
    data = {
        "documents": [
            {"id": "1", "language": "en", "text": text}
        ]
    }
    response = requests.post(url, headers=headers, json=data)
    result = response.json()
    try:
        sentiment = result["documents"][0]["sentiment"]
        confidence = result["documents"][0]["confidenceScores"]
        return sentiment, confidence
    except Exception as e:
        return "Error", {}

@app.route("/", methods=["GET", "POST"])
def index():
    sentiment = None
    confidence = None
    if request.method == "POST":
        text = request.form.get("text")
        sentiment, confidence = analyze_sentiment(text)
    return render_template("index.html", sentiment=sentiment, confidence=confidence)

if __name__ == "__main__":
    app.run(debug=True)
