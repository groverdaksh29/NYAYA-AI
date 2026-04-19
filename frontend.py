import streamlit as st
from backend import analyze_scenario
import re

# 🔥 CLEAN FUNCTION (removes ANY HTML)
def clean_text(text):
    if not text:
        return ""
    return re.sub(r"<.*?>", "", str(text)).strip()


st.set_page_config(
    page_title="NyayaAI – Indian Legal Assistant",
    page_icon="⚖️",
    layout="centered",
)

# 🎨 STYLES
st.markdown("""
<style>
html, body { font-family: 'DM Sans', sans-serif; }
.stApp { background: linear-gradient(135deg, #0F1B3D 0%, #1A2D5A 50%, #0F1B3D 100%); }

.card { background:rgba(255,255,255,0.04); border:1px solid rgba(212,160,23,0.2); border-radius:18px; padding:22px 26px; margin-bottom:20px; }

.article-box { background:rgba(255,255,255,0.05); border-left:3px solid #D4A017; border-radius:10px; padding:14px 16px; margin-bottom:12px; }
.article-num { font-weight:800; color:#F0C040; }
.article-title { font-weight:600; color:#FDF6E3; }
.article-summary { font-size:0.9rem; color:rgba(253,246,227,0.7); }
.article-rel { font-size:0.85rem; color:#FF8C42; }

.law-box { background:rgba(255,255,255,0.04); border-left:3px solid #FF6B1A; border-radius:10px; padding:12px 16px; margin-bottom:10px; }

.action-item { background:rgba(255,255,255,0.04); border-radius:10px; padding:12px; margin-bottom:8px; }
</style>
""", unsafe_allow_html=True)

st.markdown("## ⚖️ NyayaAI")

api_key = st.text_input("Enter Groq API Key", type="password")
scenario = st.text_area("Describe your legal scenario")

if st.button("Analyze"):
    if not api_key or not scenario:
        st.warning("Enter API key and scenario")
    else:
        data = analyze_scenario(api_key, scenario)

        # 🔥 BASIC CLEAN
        data["riskTitle"] = clean_text(data.get("riskTitle"))
        data["riskExplanation"] = clean_text(data.get("riskExplanation"))
        data["explanation"] = clean_text(data.get("explanation"))

        # 🔥 FORCE SAFE STRUCTURE
        articles = data.get("articles", [])
        if not isinstance(articles, list):
            articles = []

        laws = data.get("laws", [])
        if not isinstance(laws, list):
            laws = []

        steps = data.get("actionSteps", [])
        if not isinstance(steps, list):
            steps = []

        # ⚠️ RISK
        st.markdown(f"""
        <div class="card">
        <h3>⚠️ {data['riskTitle']}</h3>
        <p>{data['riskExplanation']}</p>
        </div>
        """, unsafe_allow_html=True)

        # 📖 EXPLANATION
        st.markdown(f"""
        <div class="card">
        <h4>📖 Explanation</h4>
        <p>{data['explanation']}</p>
        </div>
        """, unsafe_allow_html=True)

        # 📜 ARTICLES (SAFE RENDER)
        articles_html = ""

        for a in articles:
            if not isinstance(a, dict):
                continue

            number = clean_text(a.get("number"))
            title = clean_text(a.get("title"))
            summary = clean_text(a.get("summary"))
            relevance = clean_text(a.get("relevance"))

            articles_html += f"""
            <div class="article-box">
                <div class="article-num">{number}</div>
                <div class="article-title">{title}</div>
                <div class="article-summary">{summary}</div>
                <div class="article-rel">{relevance}</div>
            </div>
            """

        if articles_html:
            st.markdown(f"""
            <div class="card">
            <h4>📜 Articles</h4>
            {articles_html}
            </div>
            """, unsafe_allow_html=True)

        # ⚖️ LAWS
        laws_html = ""

        for l in laws:
            if not isinstance(l, dict):
                continue

            name = clean_text(l.get("name"))
            section = clean_text(l.get("section"))
            relevance = clean_text(l.get("relevance"))

            laws_html += f"""
            <div class="law-box">
                <b>{name}</b><br>
                {section}<br>
                {relevance}
            </div>
            """

        if laws_html:
            st.markdown(f"""
            <div class="card">
            <h4>⚖️ Laws</h4>
            {laws_html}
            </div>
            """, unsafe_allow_html=True)

        # 🧭 ACTION STEPS
        steps_html = ""

        for i, step in enumerate(steps, 1):
            steps_html += f"""
            <div class="action-item">
                {i}. {clean_text(step)}
            </div>
            """

        if steps_html:
            st.markdown(f"""
            <div class="card">
            <h4>🧭 Action Steps</h4>
            {steps_html}
            </div>
            """, unsafe_allow_html=True)