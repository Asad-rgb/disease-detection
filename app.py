import os
from flask import Flask, render_template, request
from kindwise import CropHealthApi

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = "static/uploads"

# Initialize the CropHealthApi with your API key
KINDAWISE_API_KEY = "BefPrr4m7Iy3Jlyt8ehz82jfJ6VcmfVoux72YVDcGLwhJGkymT"  # Replace with your actual API key
api = CropHealthApi(api_key=KINDAWISE_API_KEY)

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

        return render_template("result.html", image_url=image_path, disease=disease, confidence=confidence, description=description, treatment=treatment)

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
