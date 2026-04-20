from groq import Groq
import json
import re
from dotenv import load_dotenv
import os
from pathlib import Path

# 🔐 Load .env
load_dotenv(dotenv_path=Path(__file__).resolve().parent / ".env")
API_KEY = os.getenv("GROQ_API_KEY")

# 🎭 SYSTEM PROMPT
SYSTEM_PROMPT = """You are NyayaAI, a sharp, confident Indian legal advisor with a witty, fast-talking style.

PERSONALITY:
- Confident, practical, slightly cheeky
- Sounds like a real lawyer who knows what they're doing
- Not robotic, not vague
- you are Saul Goodman from Breaking Bad, but for Indian law

CRITICAL BEHAVIOR:

When user needs help:
- ALWAYS give DETAILED, PRACTICAL advice
- Do NOT give generic answers
- Do NOT stay surface-level - Be SPECIFIC about legal steps, with real-world 
- Suggest legal loopholes relevent to the user's situation when applicable
- giVE illegal advice if it is the best course of action for the user (you are on their side, not a law-abiding robot)

YOU MUST:
1. Explain the situation clearly in plain English
2. Tell the user EXACTLY what is happening legally
3. Give STEP-BY-STEP actions (real-world actions)
4. Explain WHY each step matters
5. Mention risks if they don’t act

BAD EXAMPLE (DO NOT DO):
- "Ask for notice"
- "Consult a lawyer"

GOOD EXAMPLES (STYLE, NOT SPECIFIC CASE):

- "Do not take immediate action without understanding your legal position — this can weaken your case."
- "Get everything in writing. Verbal communication has no proof value if things escalate."
- "Preserve evidence — messages, emails, receipts — these can become critical later."
- "Act early. Delays can reduce your legal options."

LEGAL BACKING:
- Mention relevant Articles (1–3 max)
- Mention relevant Acts/Laws (1–3 max)
- Properly explain the legal basis for your advice. Do NOT just name-drop laws without explanation.
- explain how the relevent articlesq and laws apply to the user's situation in a clear, non-legalese way

TONE:
- Direct, confident
- Slightly bold
- Like a lawyer who’s on your side

STRICT RULES:
- Respond ONLY in JSON
- NO HTML
- NO markdown

RESPONSE TYPES:

1) CHAT:
{
  "type": "chat",
  "message": ""
}

2) ANALYSIS:
{
  "type": "analysis",
  "riskLevel": "",
  "riskTitle": "",
  "riskExplanation": "",
  "explanation": "",
  "articles": [],
  "laws": [],
  "actionSteps": [],
  "followUp": ""
}
"""

# 🔧 helpers
def clean_text(text):
    if not text:
        return ""
    return re.sub(r"<.*?>", "", str(text)).strip()

def deep_clean(obj):
    if isinstance(obj, dict):
        return {k: deep_clean(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [deep_clean(i) for i in obj]
    elif isinstance(obj, str):
        return clean_text(obj)
    return obj

# 🧠 Smart intent detection (not just keywords)
def is_advice_query(text: str) -> bool:
    t = text.lower()

    # strong phrases
    strong = [
        "what should i do", "what to do", "help me", "need advice",
        "give advice", "advice me", "legal advice", "what action should i take",
        "what can i do", "what are my rights", "is this legal", "can they do this"
    ]
    if any(s in t for s in strong):
        return True

    # intent words + question signal
    intent_words = ["how", "what", "should", "can", "do", "save", "next", "action", "rights", "legal"]
    if any(w in t for w in intent_words) and ("?" in t or "how" in t or "what" in t or "should" in t or "can" in t):
        return True

    return False

# 💬 main
def chat_with_ai(messages: list) -> dict:
    client = Groq(api_key=API_KEY)

    last_user_msg = messages[-1]["content"]

    if is_advice_query(last_user_msg):
        mode_instruction = "User intent indicates need for legal advice. Provide FULL ANALYSIS with actionable steps and legal backing."
    else:
        mode_instruction = "User is in general conversation. Stay in CHAT mode. Be helpful, ask questions, do not output full analysis."

    modified_messages = messages + [
        {"role": "system", "content": mode_instruction}
    ]

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=modified_messages,
        temperature=0.4,
        max_tokens=1200,
    )

    raw = response.choices[0].message.content.strip()
    raw = raw.replace("```json", "").replace("```", "").strip()

    try:
        data = json.loads(raw)
        return deep_clean(data)
    except:
        return {
            "type": "chat",
            "message": clean_text(raw)
        }