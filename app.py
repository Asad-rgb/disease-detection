import os
import requests
from flask import Flask, render_template, request

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = "static/uploads"

# 🔹 Your API Key for Kindawise
KINDAWISE_API_KEY = "BefPrr4m7Iy3Jlyt8ehz82jfJ6VcmfVoux72YVDcGLwhJGkymT"  # Replace with your actual API key

# 🔹 Telegram Bot Credentials
TELEGRAM_BOT_TOKEN = "7996633142:AAFZjbjFPb5SocenBGs2W-v-qV_hGNuqrbQ"  # Replace with your Telegram Bot Token
TELEGRAM_CHAT_ID = "6631656756"      # Replace with your Telegram Chat ID

def send_telegram_alert(disease, confidence, image_url):
    """ Sends a Telegram message with disease detection results """
    message = f"🌿 Plant Disease Alert!\n\n🔬 Disease: {disease}\n📊 Confidence: {confidence}%\n🖼 Image: {image_url}"
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    data = {"chat_id": TELEGRAM_CHAT_ID, "text": message, "parse_mode": "Markdown"}
    requests.post(url, data=data)

def detect_disease(image_path):
    """ Sends the uploaded image to Kindawise API for disease detection """
    url = "https://api.kindawise.com/crop.health/v1/detect"
    headers = {"Authorization": f"Bearer {KINDAWISE_API_KEY}"}
    files = {"image": open(image_path, "rb")}
    
    response = requests.post(url, headers=headers, files=files)
    result = response.json()

    if "disease" in result:
        return result["disease"], result["confidence"]
    return "Unknown", 0

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        image = request.files["image"]
        if image:
            image_path = os.path.join(app.config["UPLOAD_FOLDER"], image.filename)
            image.save(image_path)

            # 🔹 Detect Disease using Kindawise API
            disease, confidence = detect_disease(image_path)

            # 🔹 Send Telegram Alert
            send_telegram_alert(disease, confidence, image_path)

            return render_template("result.html", image_url=image_path, disease=disease, confidence=confidence)

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
