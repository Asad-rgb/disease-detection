import os
import requests
from flask import Flask, render_template, request
from kindwise import CropHealthApi

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = "static/uploads"

# Replace with your actual Telegram credentials
TELEGRAM_BOT_TOKEN = "7996633142:AAFZjbjFPb5SocenBGs2W-v-qV_hGNuqrbQ"
TELEGRAM_CHAT_ID = "6631656756"

KINDAWISE_API_KEY = "cStd84k8CEnEon4V0Jb0QJ6kmxwQUzpVZiyKHvoaZ7jKMEGRg1"  # Replace with your API key
api = CropHealthApi(api_key=KINDAWISE_API_KEY)

def send_telegram_alert(image_path, disease, confidence, description, treatment):
    """Send a Telegram alert with image and disease details."""
    
    message = (
        f"🚨 Plant Disease Detected! 🚨\n\n"
        f"🌿 Disease: {disease}\n"
        f"📊 Confidence: {confidence:.2f}%\n\n"
        f"📝 Description:\n{description}\n\n"
        f"💊 Treatment: {treatment}"
    )

    # First, send text message
    text_url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    text_data = {"chat_id": TELEGRAM_CHAT_ID, "text": message, "parse_mode": "Markdown"}
    text_response = requests.post(text_url, data=text_data)
    
    print("Text message response:", text_response.json())  # Debugging

    # Then, send the image
    photo_url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendPhoto"
    with open(image_path, "rb") as image:
        photo_data = {"chat_id": TELEGRAM_CHAT_ID}
        photo_files = {"photo": image}
        photo_response = requests.post(photo_url, data=photo_data, files=photo_files)

        print("Photo message response:", photo_response.json())  # Debugging

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        if "image" not in request.files:
            return "No file part", 400

        image = request.files["image"]
        if image.filename == "":
            return "No selected file", 400

        # Save the uploaded image
        image_path = os.path.join(app.config["UPLOAD_FOLDER"], image.filename)
        image.save(image_path)

        # Perform disease detection using Kindwise API
        identification = api.identify(image_path, details=["description", "treatment"])

        # Extract disease information from the response
        if identification.result.disease.suggestions:
            disease = identification.result.disease.suggestions[0].name
            confidence = identification.result.disease.suggestions[0].probability * 100
            description = identification.result.disease.suggestions[0].details.get("description", "No description available.")
            treatment = identification.result.disease.suggestions[0].details.get("treatment", "No treatment information available.")
        else:
            disease = "Unknown"
            confidence = 0
            description = "No description available."
            treatment = "No treatment information available."

        # Send Telegram Alert
        send_telegram_alert(image_path, disease, confidence, description, treatment)

        return render_template("result.html", image_url=image_path, disease=disease, confidence=confidence, description=description, treatment=treatment)

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
