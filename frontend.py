import streamlit as st
from backend import chat_with_ai, SYSTEM_PROMPT
import re, html

# ---------- CLEAN ----------
def clean_text(text):
    if not text:
        return ""
    text = re.sub(r"<.*?>", "", str(text))
    text = html.unescape(text)
    return text.strip()

# ---------- PAGE ----------
st.set_page_config(page_title="NyayaAI", layout="centered")

# ---------- PREMIUM CSS ----------
st.markdown("""
<style>

/* 🌌 Background */
.stApp {
    background: radial-gradient(circle at top, #0f172a 0%, #020617 100%);
}

/* Container */
.block-container {
    max-width: 820px;
    padding-top: 2rem;
}

/* Title */
.title {
    text-align: center;
    font-size: 3rem;
    font-weight: 700;
    background: linear-gradient(90deg, #facc15, #fbbf24);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.subtitle {
    text-align: center;
    color: #94a3b8;
    margin-bottom: 25px;
}

/* Glass effect */
.glass {
    background: rgba(255,255,255,0.03);
    backdrop-filter: blur(12px);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 14px;
    padding: 14px 18px;
    margin: 12px 0;
}

/* 👤 User bubble */
.user {
    background: linear-gradient(135deg, #1e293b, #0f172a);
    border-radius: 14px;
    padding: 12px 16px;
    margin: 10px 0;
    color: #e2e8f0;
    text-align: right;
}

/* 🤖 AI bubble */
.bot {
    background: rgba(255,255,255,0.04);
    border-left: 3px solid #facc15;
    border-radius: 14px;
    padding: 14px 16px;
    margin: 10px 0;
    color: #e2e8f0;
    box-shadow: 0 0 20px rgba(250,204,21,0.05);
}

/* Section titles */
.section-title {
    margin-top: 12px;
    font-weight: 600;
    color: #facc15;
}

/* Buttons */
.stButton>button {
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.1);
    border-radius: 12px;
    color: #e2e8f0;
    transition: all 0.2s ease;
}

.stButton>button:hover {
    border: 1px solid #facc15;
    color: #facc15;
    transform: translateY(-1px);
}

/* Input */
.stChatInput {
    position: fixed;
    bottom: 20px;
    left: 50%;
    transform: translateX(-50%);
    width: 60%;
}

</style>
""", unsafe_allow_html=True)

# ---------- HEADER ----------
st.markdown('<div class="title">⚖️ NyayaAI</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Your Personal Legal Breakdown Assistant</div>', unsafe_allow_html=True)

# ---------- QUICK ACTIONS ----------
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("🏠 Landlord"):
        st.session_state.prefill = "My landlord is trying to evict me before lease ends"

with col2:
    if st.button("💼 Job Issue"):
        st.session_state.prefill = "My employer hasn't paid my salary for 2 months"

with col3:
    if st.button("👮 Police"):
        st.session_state.prefill = "Can police check my phone without permission?"

st.markdown("---")

# ---------- MEMORY ----------
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": SYSTEM_PROMPT}]

if "display" not in st.session_state:
    st.session_state.display = []

# ---------- FIRST MESSAGE ----------
if len(st.session_state.display) == 0:
    st.session_state.display.append({
        "role": "assistant",
        "content": {
            "type": "chat",
            "message": "Alright, what’s going on? Tell me the situation — I’ll break it down for you."
        }
    })

# ---------- CHAT ----------
for msg in st.session_state.display:

    if msg["role"] == "user":
        st.markdown(f'<div class="user">{msg["content"]}</div>', unsafe_allow_html=True)

    else:
        data = msg["content"]

        if data.get("type") == "chat":
            st.markdown(f'<div class="bot">{clean_text(data.get("message"))}</div>', unsafe_allow_html=True)

        else:
            st.markdown(f'<div class="bot"><b>⚠️ {clean_text(data.get("riskTitle"))}</b><br>{clean_text(data.get("riskExplanation"))}</div>', unsafe_allow_html=True)

            st.markdown('<div class="section-title">📖 Explanation</div>', unsafe_allow_html=True)
            st.write(clean_text(data.get("explanation")))

            if data.get("articles"):
                st.markdown('<div class="section-title">📜 Articles</div>', unsafe_allow_html=True)
                for a in data.get("articles", []):
                    if isinstance(a, dict):
                        st.write(f"- {clean_text(a.get('number'))}: {clean_text(a.get('title'))}")
                    else:
                        st.write(f"- {clean_text(a)}")

            if data.get("laws"):
                st.markdown('<div class="section-title">⚖️ Laws</div>', unsafe_allow_html=True)
                for l in data.get("laws", []):
                    if isinstance(l, dict):
                        st.write(f"- {clean_text(l.get('name'))}")
                    else:
                        st.write(f"- {clean_text(l)}")

            st.markdown('<div class="section-title">🧭 What you should do</div>', unsafe_allow_html=True)
            for step in data.get("actionSteps", []):
                st.write(f"- {clean_text(step)}")

# ---------- INPUT ----------
user_input = st.chat_input("Describe your legal situation...")

if "prefill" in st.session_state:
    user_input = st.session_state.pop("prefill")

if user_input:

    st.session_state.messages.append({"role": "user", "content": user_input})
    st.session_state.display.append({"role": "user", "content": user_input})

    with st.spinner("Thinking like a lawyer..."):
        response = chat_with_ai(st.session_state.messages)

    if response.get("type") == "chat":
        memory_text = response.get("message", "")
    else:
        memory_text = response.get("explanation", "")

    st.session_state.messages.append({"role": "assistant", "content": memory_text})
    st.session_state.display.append({"role": "assistant", "content": response})

    st.rerun()