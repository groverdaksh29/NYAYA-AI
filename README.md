div align="center">

# ⚖️ NyayaAI
### *Your Street-Smart Indian Legal Advisor*

![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![Groq](https://img.shields.io/badge/Groq-LLaMA_3.3_70B-F55036?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

**NyayaAI** is an AI-powered Indian legal assistant that gives you sharp, actionable legal advice — not textbook nonsense. It maps your situation to the Constitution of India, relevant Acts, and finds every loophole available.

[🚀 Try it Live](https://nyayaai.streamlit.app) &nbsp;·&nbsp; [🐛 Report a Bug](https://github.com/groverdaksh29/NYAYA-AI/issues) &nbsp;·&nbsp; [💡 Request a Feature](https://github.com/groverdaksh29/NYAYA-AI/issues)

---

</div>

## ✨ Features

- 🧠 **AI Legal Analysis** — Powered by LLaMA 3.3 70B via Groq for fast, intelligent responses
- 📜 **Constitutional Mapping** — Automatically cites relevant Articles of the Indian Constitution
- ⚖️ **Law & Section References** — Links your situation to specific Acts and Sections
- 🔍 **Loophole Detection** — Finds grey areas and clever legal angles in your favour
- 🟢🟡🔴 **Risk Assessment** — Instantly tells you how serious your situation is
- 🧭 **Step-by-Step Action Plan** — Tells you exactly what to do next
- 💬 **Conversational Interface** — Chat naturally, like talking to a real lawyer
- 📋 **Session History** — Switch between multiple consultations in the same session

---

## 🚀 Getting Started

### Prerequisites
- Python 3.9 or above
- A free Groq API key → [console.groq.com](https://console.groq.com)

### Installation

**1. Clone the repository**
```bash
git clone https://github.com/groverdaksh29/NYAYA-AI.git
cd NYAYA-AI
```

**2. Install dependencies**
```bash
pip install -r requirements.txt
```

**3. Set up your API key**

Create a `.env` file in the project root:
```env
GROQ_API_KEY=your_actual_key_here
```

**4. Run the app**
```bash
streamlit run frontend.py
```

The app will open at **http://localhost:8501** 🎉

---

## ☁️ Deploy Online for Free

### Streamlit Cloud (Recommended)

| Step | Action |
|------|--------|
| 1 | Push this repo to your GitHub account |
| 2 | Go to [streamlit.io/cloud](https://streamlit.io/cloud) and sign in with GitHub |
| 3 | Click **New App** → select your repo → set main file as `frontend.py` |
| 4 | Click **Advanced Settings** → add your secret: `GROQ_API_KEY = "your_key"` |
| 5 | Hit **Deploy** — live in ~2 minutes ✅ |

> ℹ️ Every time you push to GitHub, Streamlit Cloud auto-redeploys. No manual steps needed.

---

## 📁 Project Structure

```
NYAYA-AI/
│
├── frontend.py          # Main Streamlit UI — chat interface, styling, session logic
├── backend.py           # AI logic — Groq API integration, prompt engineering
├── requirements.txt     # Python dependencies
├── .env                 # Local API key (DO NOT upload to GitHub)
├── .gitignore           # Ensures .env is never committed
└── README.md            # You are here
```

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | Streamlit + Custom CSS |
| AI Model | LLaMA 3.3 70B (via Groq) |
| Backend | Python |
| Deployment | Streamlit Community Cloud |

---

## ⚠️ Disclaimer

> NyayaAI is built for **educational purposes only** and does not constitute professional legal advice. Always consult a qualified lawyer for serious legal matters.

---

<div align="center">

Made with ❤️ for India &nbsp;·&nbsp; *Satyameva Jayate* ☸️

</div>
