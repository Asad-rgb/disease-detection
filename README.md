# Disease Detection Website

This is a Flask-based web application for detecting plant diseases using the *Kindwise API*. The app allows users to upload images, detects diseases, and sends Telegram alerts with the results.

---

## 🚀 Features
- *Upload Plant Images* for Disease Detection
- *Uses Kindwise API* for disease classification
- *Telegram Alerts* for detected diseases
- *Beautiful UI with CSS Styling*
- *Deployed on Render (Free Hosting)*

---

## 📌 Requirements

Make sure you have the following installed:

- *Python (3.x)* → [Download Here](https://www.python.org/)
- *Git* → [Download Here](https://git-scm.com/)
- *GitHub Account* → [Sign Up](https://github.com/)
- *Render Account* → [Sign Up](https://render.com/)

Additionally, install the required Python packages:

bash
pip install flask requests python-telegram-bot gunicorn


---

## 📂 Project Structure


disease-detection/

├── app.py                  # Flask Backend

├── requirements.txt         # Dependencies

├── Procfile                 # Render Deployment Config

├── templates/

│   ├── index.html          # Upload Page

│   ├── result.html         # Results Page

├── static/

│   ├── styles.css          # CSS Styling

│   ├── uploads/            # Image Upload Folder


---

## 🔧 Setup & Run Locally

⿡ *Clone the Repository*
bash
git clone https://github.com/YOUR_USERNAME/disease-detection.git
cd disease-detection


⿢ *Install Dependencies*
bash
pip install -r requirements.txt


⿣ *Run the Application*
bash
python app.py


✅ The app will run at: *http://127.0.0.1:5000/*

---

## 🚀 Deploy on Render

⿡ *Push Your Code to GitHub*
bash
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/disease-detection.git
git push -u origin main


⿢ *Deploy on Render*
- Go to [Render](https://render.com/)
- Click *New → Web Service*
- Select *Your GitHub Repo* (disease-detection)
- Set the *Build Command:*
  bash
  pip install -r requirements.txt
  
- Set the *Start Command:*
  bash
  gunicorn app:app
  
- Click *Create Web Service* ✅

---

## 📩 Telegram Alerts Setup

⿡ *Create a Telegram Bot*
- Open Telegram and search for *@BotFather*
- Type /newbot and follow the instructions
- Get the *Bot Token*

⿢ *Get Your Chat ID*
- Open https://api.telegram.org/botYOUR_BOT_TOKEN/getUpdates
- Find chat_id from the response

⿣ **Update app.py with Your Credentials**
python
TELEGRAM_BOT_TOKEN = "YOUR_BOT_TOKEN"
TELEGRAM_CHAT_ID = "YOUR_CHAT_ID"


---

## 🎉 Done!

- *Your Website is Live on Render!* 🚀
- *Upload an Image* and get disease detection results!
- *Check Telegram* for alerts! 📩

---

## 📜 License
This project is open-source and free to use under the *MIT License*.
