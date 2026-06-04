from flask import Flask, request
import os

app = Flask(__name__)

@app.route("/")
def home():
    return "225BOT OK"

@app.route("/webhook", methods=["POST"])
def webhook():
    body = request.get_json()

    print(body)

    return "OK"

if __name__ == "__main__":
    app.run(debug=True)