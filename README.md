# ⚖️ NyayaAI – Indian Legal Reasoning & Rights Assistant

A Streamlit web app that analyzes legal scenarios and maps them to the Constitution of India and other Indian laws.

---

## 🚀 How to Run Locally

### Step 1 — Install Python
Download Python from https://python.org (version 3.9 or above)

### Step 2 — Install dependencies
Open Terminal / Command Prompt in this folder and run:
```
pip install -r requirements.txt
```

### Step 3 — Add your Groq API key
Create a `.env` file in the project folder and add:
```
GROQ_API_KEY=your_actual_key_here
```
Get a free key at https://console.groq.com

### Step 4 — Run the app
```
streamlit run frontend.py
```
The app will open automatically in your browser at http://localhost:8501

---

## 🌐 How to Deploy Online (Free) — Streamlit Cloud

1. Create a free account at https://github.com and upload this folder as a repository
2. Go to https://streamlit.io/cloud → Sign in with GitHub
3. Click "New app" → Select your repository → Set main file as `frontend.py`
4. Before deploying, click "Advanced settings" → add your secret:
   ```
   GROQ_API_KEY = "your_actual_key_here"
   ```
5. Click Deploy — your app goes live in ~2 minutes!

---

## 📁 Project Files
| File | Purpose |
|------|---------|
| `frontend.py` | Main Streamlit application (UI) |
| `backend.py` | AI logic and Groq API integration |
| `requirements.txt` | Python dependencies |
| `.env` | Your local API key (do NOT upload to GitHub) |

---

## ⚠️ Disclaimer
This tool is for **educational purposes only** and does not constitute legal advice.