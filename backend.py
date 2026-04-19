from groq import Groq
import json
import re

SYSTEM_PROMPT = """You are NyayaAI, an expert on Indian constitutional and statutory law.

Respond ONLY with valid JSON. No markdown. No HTML. Only plain text.

Structure:
{
  "riskLevel": "low" or "grey" or "high",
  "riskTitle": "",
  "riskExplanation": "",
  "explanation": "",
  "articles": [
    {
      "number": "",
      "title": "",
      "summary": "",
      "relevance": ""
    }
  ],
  "laws": [
    {
      "name": "",
      "section": "",
      "relevance": ""
    }
  ],
  "actionSteps": []
}
"""

def remove_html(text):
    # remove full HTML tags
    text = re.sub(r"<.*?>", "", text)

    # remove leftover class= junk
    text = re.sub(r'class=".*?"', "", text)

    # remove random div words
    text = text.replace("div", "")

    return text.strip()


def deep_clean(obj):
    if isinstance(obj, dict):
        return {k: deep_clean(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [deep_clean(i) for i in obj]
    elif isinstance(obj, str):
        return remove_html(obj)
    return obj


def analyze_scenario(api_key: str, scenario: str) -> dict:
    client = Groq(api_key=api_key)

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": scenario}
        ],
        temperature=0.2,
        max_tokens=1200,
    )

    raw = response.choices[0].message.content.strip()

    # remove markdown wrappers
    raw = raw.replace("```json", "").replace("```", "").strip()

    try:
        data = json.loads(raw)

        # 🔥 CLEAN ENTIRE JSON (THIS IS THE REAL FIX)
        data = deep_clean(data)

        return data

    except:
        return {
            "riskLevel": "grey",
            "riskTitle": "Parsing Error",
            "riskExplanation": "Model returned invalid format.",
            "explanation": remove_html(raw),
            "articles": [],
            "laws": [],
            "actionSteps": ["Try rephrasing your question"]
        }