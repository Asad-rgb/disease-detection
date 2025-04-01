from flask import Flask, request, render_template
import requests
import os
from werkzeug.utils import secure_filename
from telegram import Bot

app = Flask(__name__)

# Configurations
API_KEY = "YOUR_KINDWISE_API_KEY"
KINDWISE_API_URL = "https://api.kindwise.com/detect"

TELEGRAM_BOT_TOKEN = "7996633142:AAFZjbjFPb5SocenBGs2W-v-qV_hGNuqrbQ"
TELEGRAM_CHAT_ID = "6631656756"
bot = Bot(token=TELEGRAM_BOT_TOKEN)

UPLOAD_FOLDER = "static/uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/upload", methods=["POST"])
def upload():
    if "file" not in request.files:
        return "No file uploaded", 400
    
    file = request.files["file"]
    filename = secure_filename(file.filename)
    file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
    file.save(file_path)

    with open(file_path, "rb") as f:
        response = requests.post(KINDWISE_API_URL, files={"file": f}, headers={"Authorization": f"Bearer {API_KEY}"})

    if response.status_code == 200:
        result = response.json()
        disease = result.get("disease", "Unknown")
        confidence = result.get("confidence", "N/A")

        # Send Telegram Alert
        message = f"Disease detected: {disease}\nConfidence: {confidence}"
        bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=message)

        return render_template("result.html", disease=disease, confidence=confidence, image_url=file_path)
    else:
        return "Error from Kindwise API", 500

if __name__ == "__main__":
    app.run(debug=True)