import streamlit as st
from backend import get_ai_response, SYSTEM_PROMPT
import re, html, json, io
from datetime import datetime

# ── Helpers ───────────────────────────────────────────────────────────────────
def remove_html_tags(text):
    if not text:
        return ""
    text = re.sub(r"<.*?>", "", str(text))
    text = html.unescape(text)
    return text.strip()

def get_all_chats():
    return st.session_state.get("history", {})

def store_all_chats(history):
    st.session_state["history"] = history

def store_current_session():
    if not st.session_state.display or len(st.session_state.display) <= 1:
        return
    history = get_all_chats()
    chat_id = st.session_state.get("chat_id")
    title = st.session_state.get("chat_title", "Untitled")
    history[chat_id] = {
        "title": title,
        "timestamp": st.session_state.get("chat_timestamp", ""),
        "messages": st.session_state.messages,
        "display": st.session_state.display,
    }
    store_all_chats(history)

def begin_new_session():
    store_current_session()
    st.session_state.chat_id = datetime.now().strftime("%Y%m%d_%H%M%S")
    st.session_state.chat_timestamp = datetime.now().strftime("%d %b %Y, %I:%M %p")
    st.session_state.chat_title = "New Consultation"
    st.session_state.messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    st.session_state.display = []

def open_old_chat(chat_id):
    store_current_session()
    history = get_all_chats()
    if chat_id in history:
        chat = history[chat_id]
        st.session_state.chat_id = chat_id
        st.session_state.chat_title = chat.get("title", "Consultation")
        st.session_state.chat_timestamp = chat.get("timestamp", "")
        st.session_state.messages = chat.get("messages", [{"role": "system", "content": SYSTEM_PROMPT}])
        st.session_state.display = chat.get("display", [])

def remove_chat(chat_id):
    history = get_all_chats()
    if chat_id in history:
        del history[chat_id]
        store_all_chats(history)

def get_total_consultations():
    return st.session_state.get("total_consultations", 0)

def increment_consultations():
    st.session_state["total_consultations"] = get_total_consultations() + 1

# ── Init session ──────────────────────────────────────────────────────────────
if "chat_id" not in st.session_state:
    st.session_state.chat_id = datetime.now().strftime("%Y%m%d_%H%M%S")
    st.session_state.chat_timestamp = datetime.now().strftime("%d %b %Y, %I:%M %p")
    st.session_state.chat_title = "New Consultation"

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": SYSTEM_PROMPT}]

if "display" not in st.session_state:
    st.session_state.display = []

if "total_consultations" not in st.session_state:
    st.session_state.total_consultations = 0

if "active_tab" not in st.session_state:
    st.session_state.active_tab = "chat"

if len(st.session_state.display) == 0:
    st.session_state.display.append({
        "role": "assistant",
        "content": {
            "type": "chat",
            "message": "Alright — what's the situation? Give me the full picture and I'll tell you exactly where you stand legally."
        }
    })

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(page_title="NyayaAI", page_icon="⚖️", layout="wide")

# ── CSS ───────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,600;0,700;1,400&family=DM+Sans:wght@300;400;500;600&display=swap');

*, *::before, *::after { box-sizing: border-box; }
html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }
#MainMenu, footer, header { visibility: hidden; }

/* ── BACKGROUND ── */
.stApp {
    background-color: #070608;
    background-image:
        radial-gradient(ellipse at 15% 15%, rgba(180,134,20,0.09) 0%, transparent 50%),
        radial-gradient(ellipse at 85% 85%, rgba(139,90,20,0.07) 0%, transparent 50%),
        radial-gradient(ellipse at 50% 50%, rgba(100,60,10,0.04) 0%, transparent 70%);
}
.stApp::before {
    content: '☸';
    position: fixed;
    top: 50%; left: 50%;
    transform: translate(-50%, -50%);
    font-size: 65vw;
    color: rgba(180,134,20,0.018);
    pointer-events: none;
    z-index: 0;
    line-height: 1;
}

/* ── LAYOUT ── */
section[data-testid="stSidebar"] {
    background: #0c0b09 !important;
    border-right: 1px solid rgba(184,134,11,0.12) !important;
    min-width: 280px !important;
    max-width: 280px !important;
}
.block-container {
    padding: 0 2rem 7rem !important;
    max-width: 100% !important;
    position: relative;
    z-index: 1;
}

/* ── SIDEBAR ── */
.sidebar-logo {
    text-align: center;
    padding: 24px 16px 20px;
    border-bottom: 1px solid rgba(184,134,11,0.12);
    margin-bottom: 8px;
}
.sidebar-logo-title {
    font-family: 'Cormorant Garamond', serif;
    font-size: 1.7rem;
    font-weight: 700;
    color: #d4a017;
    letter-spacing: 2px;
}
.sidebar-logo-sub {
    font-size: 0.62rem;
    letter-spacing: 3px;
    text-transform: uppercase;
    color: rgba(255,255,255,0.2);
    margin-top: 4px;
}
.tricolor {
    display: flex;
    width: 60px; height: 2px;
    margin: 10px auto 0;
    border-radius: 2px; overflow: hidden;
}
.tc-s { flex:1; background:#FF6B1A; }
.tc-w { flex:1; background:#f5f0e8; }
.tc-g { flex:1; background:#138808; }

.sidebar-section-label {
    font-size: 0.62rem;
    letter-spacing: 2.5px;
    text-transform: uppercase;
    color: rgba(184,134,11,0.5);
    padding: 14px 16px 8px;
    font-weight: 600;
}

/* ── CONSULTATION COUNTER ── */
.consult-counter {
    margin: 0 12px 12px;
    padding: 10px 14px;
    background: rgba(184,134,11,0.06);
    border: 1px solid rgba(184,134,11,0.15);
    border-radius: 10px;
    text-align: center;
}
.counter-number {
    font-family: 'Cormorant Garamond', serif;
    font-size: 1.8rem;
    font-weight: 700;
    color: #d4a017;
    line-height: 1;
}
.counter-label {
    font-size: 0.62rem;
    letter-spacing: 2px;
    text-transform: uppercase;
    color: rgba(255,255,255,0.25);
    margin-top: 3px;
}

.no-history {
    font-size: 0.8rem;
    color: rgba(255,255,255,0.15);
    text-align: center;
    padding: 20px 16px;
    font-style: italic;
}

/* ── SIDEBAR BUTTONS ── */
.stButton > button {
    background: rgba(184,134,11,0.07) !important;
    border: 1px solid rgba(184,134,11,0.2) !important;
    border-radius: 8px !important;
    color: rgba(212,160,23,0.9) !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.82rem !important;
    font-weight: 500 !important;
    transition: all 0.2s ease !important;
    width: 100% !important;
}
.stButton > button:hover {
    background: rgba(184,134,11,0.14) !important;
    border-color: rgba(184,134,11,0.45) !important;
    color: #d4a017 !important;
    transform: translateY(-1px) !important;
}

/* ── MAIN HEADER ── */
.nyaya-header {
    text-align: center;
    padding: 20px 0 14px;
    position: relative;
    margin-bottom: 4px;
    margin-top: 10px;
}
.nyaya-header::after {
    content: '';
    position: absolute;
    bottom: 0; left: 50%;
    transform: translateX(-50%);
    width: 200px; height: 1px;
    background: linear-gradient(90deg, transparent, rgba(184,134,11,0.3), transparent);
}
.nyaya-title {
    font-family: 'Cormorant Garamond', serif;
    font-size: 5.5rem;
    font-weight: 700;
    color: #d4a017;
    letter-spacing: 4px;
    text-shadow: 0 0 60px rgba(212,160,23,0.35), 0 2px 4px rgba(0,0,0,0.5);
    line-height: 1;
}
.nyaya-subtitle {
    font-size: 0.82rem;
    letter-spacing: 3px;
    text-transform: uppercase;
    color: rgba(255,255,255,0.4);
    margin-top: 10px;
    font-weight: 400;
}
.header-tricolor {
    display: flex;
    width: 100px; height: 2px;
    margin: 12px auto 0;
    border-radius: 2px; overflow: hidden;
}
.legal-ornament {
    text-align: center;
    font-size: 0.8rem;
    color: rgba(184,134,11,0.45);
    letter-spacing: 8px;
    margin: 8px 0 16px;
    font-family: 'Cormorant Garamond', serif;
}

/* ── TAB NAV ── */
.tab-nav {
    display: flex;
    gap: 8px;
    margin: 0 0 16px 0;
    border-bottom: 1px solid rgba(184,134,11,0.1);
    padding-bottom: 0;
}
.tab-btn {
    padding: 8px 18px;
    font-size: 0.78rem;
    font-weight: 600;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    border: none;
    background: transparent;
    color: rgba(255,255,255,0.25);
    cursor: pointer;
    border-bottom: 2px solid transparent;
    margin-bottom: -1px;
    transition: all 0.2s;
    font-family: 'DM Sans', sans-serif;
}
.tab-btn.active {
    color: #d4a017;
    border-bottom-color: #d4a017;
}
.tab-btn:hover { color: rgba(212,160,23,0.7); }

/* ── PDF UPLOAD ── */
.upload-section {
    border: 1px dashed rgba(184,134,11,0.25);
    border-radius: 12px;
    padding: 14px 18px;
    margin-bottom: 16px;
    background: rgba(184,134,11,0.02);
}
.upload-label {
    font-size: 0.68rem;
    letter-spacing: 2px;
    text-transform: uppercase;
    color: rgba(184,134,11,0.55);
    font-weight: 600;
    margin-bottom: 6px;
}

/* ── DRAFT SECTION ── */
.draft-box {
    background: rgba(138,43,226,0.04);
    border: 1px solid rgba(138,43,226,0.15);
    border-radius: 12px;
    padding: 16px 18px;
    margin-top: 8px;
}
.draft-title {
    font-size: 0.68rem;
    letter-spacing: 2px;
    text-transform: uppercase;
    color: rgba(216,180,254,0.6);
    font-weight: 600;
    margin-bottom: 10px;
}
.draft-content {
    font-family: 'Courier New', monospace;
    font-size: 0.82rem;
    color: #d8b4fe;
    line-height: 1.8;
    white-space: pre-wrap;
}

/* ── LAWYER FINDER ── */
.lawyer-finder {
    background: rgba(47,133,90,0.04);
    border: 1px solid rgba(47,133,90,0.15);
    border-radius: 12px;
    padding: 16px 18px;
    margin-bottom: 16px;
}
.lawyer-finder-title {
    font-size: 0.68rem;
    letter-spacing: 2px;
    text-transform: uppercase;
    color: rgba(104,211,145,0.6);
    font-weight: 600;
    margin-bottom: 12px;
}
.lawyer-link {
    display: block;
    padding: 8px 12px;
    margin-bottom: 6px;
    background: rgba(47,133,90,0.06);
    border: 1px solid rgba(47,133,90,0.12);
    border-radius: 8px;
    color: #68D391;
    font-size: 0.82rem;
    text-decoration: none;
    transition: all 0.2s;
}
.lawyer-link:hover {
    background: rgba(47,133,90,0.12);
    border-color: rgba(47,133,90,0.3);
}
.lawyer-link-label {
    font-size: 0.68rem;
    color: rgba(104,211,145,0.5);
    margin-top: 2px;
}

/* ── CHAT MESSAGES ── */
.user-bubble {
    display: flex;
    justify-content: flex-end;
    margin: 10px 0;
}
.user-bubble-inner {
    background: linear-gradient(135deg, #1a1710, #12100a);
    border: 1px solid rgba(184,134,11,0.18);
    border-radius: 16px 16px 3px 16px;
    padding: 12px 18px;
    max-width: 75%;
    color: #e8dcc8;
    font-size: 0.91rem;
    line-height: 1.65;
}
.bot-bubble {
    display: flex;
    justify-content: flex-start;
    margin: 10px 0;
    gap: 10px;
    align-items: flex-start;
}
.bot-avatar {
    width: 32px; height: 32px;
    background: linear-gradient(135deg, #b8860b, #8B6914);
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 0.85rem;
    flex-shrink: 0;
    margin-top: 2px;
    box-shadow: 0 0 12px rgba(184,134,11,0.2);
}
.bot-bubble-inner {
    background: rgba(255,255,255,0.025);
    border: 1px solid rgba(255,255,255,0.055);
    border-left: 2px solid #b8860b;
    border-radius: 3px 16px 16px 16px;
    padding: 14px 18px;
    max-width: 85%;
    color: #d4c9b0;
    font-size: 0.91rem;
    line-height: 1.7;
    box-shadow: 0 4px 24px rgba(0,0,0,0.3);
}

/* ── RISK BADGE ── */
.risk-badge {
    display: inline-flex;
    align-items: center;
    gap: 7px;
    padding: 5px 13px;
    border-radius: 20px;
    font-size: 0.7rem;
    font-weight: 700;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    margin-bottom: 12px;
}
.risk-low  { background: rgba(47,133,90,0.13);  border: 1px solid rgba(47,133,90,0.35);  color: #68D391; }
.risk-grey { background: rgba(214,158,46,0.13); border: 1px solid rgba(214,158,46,0.35); color: #F6E05E; }
.risk-high { background: rgba(229,62,62,0.13);  border: 1px solid rgba(229,62,62,0.35);  color: #FC8181; }

/* ── ANALYSIS BLOCKS ── */
.section-block {
    margin-top: 14px;
    padding-top: 12px;
    border-top: 1px solid rgba(255,255,255,0.05);
}
.section-label {
    font-size: 0.64rem;
    letter-spacing: 2.5px;
    text-transform: uppercase;
    color: #b8860b;
    margin-bottom: 9px;
    font-weight: 600;
}
.explanation-text { color: #c8bda0; font-size: 0.91rem; line-height: 1.75; }
.article-item {
    background: rgba(184,134,11,0.04);
    border-left: 2px solid rgba(184,134,11,0.35);
    border-radius: 0 8px 8px 0;
    padding: 9px 13px;
    margin-bottom: 7px;
}
.article-num { font-size: 0.67rem; font-weight: 700; color: #b8860b; letter-spacing: 1px; text-transform: uppercase; }
.article-title { font-weight: 600; color: #e8dcc8; font-size: 0.87rem; margin: 2px 0; }
.article-relevance { font-size: 0.81rem; color: rgba(200,189,160,0.65); font-style: italic; }
.law-item {
    background: rgba(255,107,26,0.04);
    border-left: 2px solid rgba(255,107,26,0.28);
    border-radius: 0 8px 8px 0;
    padding: 9px 13px;
    margin-bottom: 7px;
}
.law-name { font-weight: 600; color: #e8dcc8; font-size: 0.87rem; }
.law-section { font-size: 0.73rem; color: #FF8C42; margin: 2px 0; }
.law-rel { font-size: 0.81rem; color: rgba(200,189,160,0.65); }
.step-item {
    display: flex;
    gap: 11px;
    align-items: flex-start;
    padding: 9px 0;
    border-bottom: 1px solid rgba(255,255,255,0.04);
    color: #c8bda0;
    font-size: 0.89rem;
    line-height: 1.6;
}
.step-num {
    min-width: 20px; height: 20px;
    background: linear-gradient(135deg, #b8860b, #8B6914);
    color: #0a0a0a; font-weight: 800; font-size: 0.65rem;
    border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    flex-shrink: 0; margin-top: 2px;
}
.loophole-box {
    background: rgba(138,43,226,0.06);
    border: 1px solid rgba(138,43,226,0.18);
    border-radius: 10px;
    padding: 11px 15px;
    margin-top: 4px;
    font-size: 0.87rem;
    color: #d8b4fe;
    line-height: 1.65;
}
.loophole-label {
    font-size: 0.65rem; letter-spacing: 2px; text-transform: uppercase;
    color: rgba(216,180,254,0.55); margin-bottom: 5px; font-weight: 600;
}
.followup-text {
    font-size: 0.87rem; color: rgba(184,134,11,0.75); font-style: italic;
    margin-top: 12px; padding-top: 11px;
    border-top: 1px solid rgba(184,134,11,0.1);
}

/* ── MISC ── */
.disclaimer {
    text-align: center; font-size: 0.68rem;
    color: rgba(255,255,255,0.12); margin-top: 6px; letter-spacing: 0.5px;
}
.stSpinner > div { border-top-color: #b8860b !important; }
::-webkit-scrollbar { width: 4px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: rgba(184,134,11,0.2); border-radius: 4px; }
.stSelectbox > div > div {
    background: rgba(255,255,255,0.03) !important;
    border: 1px solid rgba(184,134,11,0.2) !important;
    border-radius: 10px !important;
    color: #c8bda0 !important;
}
.stChatInputContainer {
    background: rgba(7,6,8,0.97) !important;
    border-top: 1px solid rgba(184,134,11,0.12) !important;
    padding: 12px 20px 16px !important;
    backdrop-filter: blur(16px) !important;
}
.stChatInput textarea {
    background: rgba(255,255,255,0.03) !important;
    border: 1px solid rgba(184,134,11,0.22) !important;
    border-radius: 10px !important;
    color: #e8dcc8 !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.91rem !important;
}
.stChatInput textarea:focus {
    border-color: rgba(184,134,11,0.45) !important;
    box-shadow: 0 0 0 2px rgba(184,134,11,0.07) !important;
}
</style>
""", unsafe_allow_html=True)

# ── SIDEBAR ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div class="sidebar-logo">
        <div style="font-size:1.8rem;margin-bottom:6px;">⚖️</div>
        <div class="sidebar-logo-title">NyayaAI</div>
        <div class="sidebar-logo-sub">Legal Consultations</div>
        <div class="tricolor"><span class="tc-s"></span><span class="tc-w"></span><span class="tc-g"></span></div>
    </div>
    """, unsafe_allow_html=True)

    # ── Consultation Counter ──
    total = get_total_consultations()
    st.markdown(f"""
    <div class="consult-counter">
        <div class="counter-number">{total}</div>
        <div class="counter-label">Consultations This Session</div>
    </div>
    """, unsafe_allow_html=True)

    if st.button("＋  New Consultation", key="new_chat"):
        begin_new_session()
        st.rerun()

    st.markdown('<div class="sidebar-section-label">Recent Consultations</div>', unsafe_allow_html=True)

    history = get_all_chats()
    sorted_history = sorted(history.items(), key=lambda x: x[1].get("timestamp", ""), reverse=True)

    if not sorted_history:
        st.markdown('<div class="no-history">No past consultations yet.</div>', unsafe_allow_html=True)
    else:
        for chat_id, chat_data in sorted_history:
            title = chat_data.get("title", "Consultation")
            is_active = chat_id == st.session_state.get("chat_id")
            col_a, col_b = st.columns([5, 1])
            with col_a:
                label = f"{'▶ ' if is_active else ''}{title[:28]}{'…' if len(title) > 28 else ''}"
                if st.button(label, key=f"load_{chat_id}"):
                    open_old_chat(chat_id)
                    st.rerun()
            with col_b:
                if st.button("✕", key=f"del_{chat_id}"):
                    remove_chat(chat_id)
                    if chat_id == st.session_state.get("chat_id"):
                        begin_new_session()
                    st.rerun()

    st.markdown("---")

    # ── Lawyer Finder ──
    st.markdown('<div class="sidebar-section-label">🔍 Find a Lawyer</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="lawyer-finder">
        <div class="lawyer-finder-title">Connect with a real lawyer</div>
        <a class="lawyer-link" href="https://lawrato.com" target="_blank">
            ⚖ LawRato.com
            <div class="lawyer-link-label">Free legal advice & consultation</div>
        </a>
        <a class="lawyer-link" href="https://vakil.in" target="_blank">
            ⚖ Vakil.in
            <div class="lawyer-link-label">Find verified lawyers near you</div>
        </a>
        <a class="lawyer-link" href="https://www.justdial.com/lawyers" target="_blank">
            ⚖ JustDial — Lawyers
            <div class="lawyer-link-label">Search by city & specialisation</div>
        </a>
        <a class="lawyer-link" href="https://districts.ecourts.gov.in" target="_blank">
            ⚖ eCourts — District Courts
            <div class="lawyer-link-label">Official government legal portal</div>
        </a>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="no-history" style="padding:8px 16px;">Educational purposes only.<br>Not legal advice.</div>', unsafe_allow_html=True)

# ── MAIN HEADER ───────────────────────────────────────────────────────────────
st.markdown("""
<div class="nyaya-header">
    <div class="nyaya-title">
        <span style="vertical-align: 0.12em; font-size: 0.9em;">☸</span>
        &nbsp;NyayaAI&nbsp;
        <span style="vertical-align: 0.12em; font-size: 0.9em;">⚖</span>
    </div>
    <div class="nyaya-subtitle">Indian Legal Reasoning & Rights Assistant</div>
    <div class="header-tricolor" style="display:flex;width:100px;height:2px;margin:12px auto 0;border-radius:2px;overflow:hidden;">
        <span style="flex:1;background:#FF6B1A;"></span>
        <span style="flex:1;background:#f5f0e8;"></span>
        <span style="flex:1;background:#138808;"></span>
    </div>
</div>
<div class="legal-ornament">— SATYAMEVA JAYATE —</div>
""", unsafe_allow_html=True)

# ── PDF UPLOAD ────────────────────────────────────────────────────────────────
st.markdown('<div class="upload-label" style="font-size:0.68rem;letter-spacing:2px;text-transform:uppercase;color:rgba(184,134,11,0.5);font-weight:600;margin-bottom:6px;">📄 Upload a Legal Document for Analysis</div>', unsafe_allow_html=True)
uploaded_pdf = st.file_uploader("", type=["pdf"], label_visibility="collapsed", key="pdf_uploader")

if uploaded_pdf is not None and uploaded_pdf.name != st.session_state.get("last_pdf_name"):
    st.session_state["last_pdf_name"] = uploaded_pdf.name
    try:
        import pypdf
        reader = pypdf.PdfReader(io.BytesIO(uploaded_pdf.read()))
        pdf_text = "\n".join(page.extract_text() or "" for page in reader.pages).strip()
        if pdf_text:
            prompt = f"I've uploaded a legal document titled '{uploaded_pdf.name}'. Please analyse it thoroughly — tell me what it means, what my rights and risks are, and what I should do.\n\nDocument content:\n{pdf_text[:4000]}"
            st.session_state.messages.append({"role": "user", "content": prompt})
            st.session_state.display.append({"role": "user", "content": f"📄 Uploaded: {uploaded_pdf.name}"})
            with st.spinner("Reading your document like a lawyer…"):
                response = get_ai_response(st.session_state.messages)
            memory_text = response.get("message", "") if response.get("type") == "chat" else response.get("explanation", "")
            st.session_state.messages.append({"role": "assistant", "content": memory_text})
            st.session_state.display.append({"role": "assistant", "content": response})
            increment_consultations()
            store_current_session()
            st.rerun()
        else:
            st.warning("Couldn't extract text from this PDF. It may be a scanned image.")
    except Exception as e:
        st.error(f"Error reading PDF: {e}")

# ── CHAT MESSAGES ─────────────────────────────────────────────────────────────
for msg in st.session_state.display:
    if msg["role"] == "user":
        st.markdown(f"""
        <div class="user-bubble">
            <div class="user-bubble-inner">{remove_html_tags(msg["content"])}</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        data = msg["content"]

        # ── Chat message ──
        if data.get("type") == "chat":
            st.markdown(f"""
            <div class="bot-bubble">
                <div class="bot-avatar">⚖</div>
                <div class="bot-bubble-inner">{remove_html_tags(data.get("message", ""))}</div>
            </div>
            """, unsafe_allow_html=True)

        # ── Document draft ──
        elif data.get("type") == "draft":
            doc_title = remove_html_tags(data.get("documentTitle", "Legal Document"))
            doc_content = remove_html_tags(data.get("content", ""))
            h = '<div class="bot-bubble"><div class="bot-avatar">⚖</div><div class="bot-bubble-inner">'
            h += f'<div class="section-label">📝 Document Draft — {doc_title}</div>'
            h += f'<div class="draft-box"><div class="draft-content">{doc_content}</div></div>'
            h += '</div></div>'
            st.markdown(h, unsafe_allow_html=True)

        # ── Full analysis ──
        else:
            risk = data.get("riskLevel", "grey")
            risk_emoji = {"low": "🟢", "grey": "🟡", "high": "🔴"}.get(risk, "⚪")
            h = '<div class="bot-bubble"><div class="bot-avatar">⚖</div><div class="bot-bubble-inner">'
            h += f'<div class="risk-badge risk-{risk}">{risk_emoji} {remove_html_tags(data.get("riskTitle",""))}</div>'
            h += f'<div class="explanation-text">{remove_html_tags(data.get("riskExplanation",""))}</div>'
            h += f'<div class="section-block"><div class="section-label">📖 Legal Breakdown</div><div class="explanation-text">{remove_html_tags(data.get("explanation",""))}</div></div>'

            articles = data.get("articles", [])
            if articles:
                h += '<div class="section-block"><div class="section-label">📜 Constitutional Articles</div>'
                for a in articles:
                    if isinstance(a, dict):
                        h += f'<div class="article-item"><div class="article-num">{remove_html_tags(a.get("number",""))}</div><div class="article-title">{remove_html_tags(a.get("title",""))}</div><div class="article-relevance">↳ {remove_html_tags(a.get("relevance",""))}</div></div>'
                h += '</div>'

            laws = data.get("laws", [])
            if laws:
                h += '<div class="section-block"><div class="section-label">⚖️ Relevant Laws</div>'
                for l in laws:
                    if isinstance(l, dict):
                        h += f'<div class="law-item"><div class="law-name">{remove_html_tags(l.get("name",""))}</div>{"<div class=law-section>" + remove_html_tags(l.get("section","")) + "</div>" if l.get("section") else ""}<div class="law-rel">{remove_html_tags(l.get("relevance",""))}</div></div>'
                h += '</div>'

            steps = data.get("actionSteps", [])
            if steps:
                h += '<div class="section-block"><div class="section-label">🧭 What You Should Do</div>'
                for i, step in enumerate(steps, 1):
                    h += f'<div class="step-item"><span class="step-num">{i}</span><span>{remove_html_tags(step)}</span></div>'
                h += '</div>'

            loophole = data.get("loophole")
            if loophole and loophole not in ("null", "None", None):
                h += f'<div class="section-block"><div class="loophole-box"><div class="loophole-label">🔍 Legal Grey Area / Loophole</div>{remove_html_tags(loophole)}</div></div>'

            followup = data.get("followUp")
            if followup:
                h += f'<div class="followup-text">💬 {remove_html_tags(followup)}</div>'

            h += '</div></div>'
            st.markdown(h, unsafe_allow_html=True)

st.markdown('<div class="disclaimer">Educational purposes only · Not legal advice · NyayaAI</div>', unsafe_allow_html=True)

# ── EXAMPLE DROPDOWN ──────────────────────────────────────────────────────────
examples = [
    "— Select an example query —",
    "Can police check my phone without a warrant?",
    "My landlord is trying to evict me before my lease ends",
    "My employer hasn't paid my salary for 2 months",
    "Can I be fired for going on strike?",
    "Someone posted defamatory content about me online",
    "Police arrested me without showing a warrant — what are my rights?",
    "My employer is forcing me to work overtime without pay",
    "Can the government acquire my land without compensation?",
    "I was denied bail — what can I do?",
    "My business partner cheated me out of profits",
    "Can I record a conversation as evidence in court?",
    "My neighbour is encroaching on my property",
    "I received a legal notice — what should I do?",
    "Draft a legal notice to my landlord for illegal eviction",
    "Draft a complaint letter to the Labour Commissioner",
]

selected = st.selectbox("", examples, label_visibility="collapsed", key="example_select")
user_input = st.chat_input("Describe your legal situation or ask me to draft a document…")

if selected != "— Select an example query —" and selected != st.session_state.get("last_example_used"):
    st.session_state["last_example_used"] = selected
    user_input = selected

if "prefill" in st.session_state:
    user_input = st.session_state.pop("prefill")

if user_input:
    if st.session_state.get("chat_title") == "New Consultation":
        st.session_state.chat_title = user_input[:40] + ("…" if len(user_input) > 40 else "")

    st.session_state.messages.append({"role": "user", "content": user_input})
    st.session_state.display.append({"role": "user", "content": user_input})

    with st.spinner("Thinking like a lawyer…"):
        response = get_ai_response(st.session_state.messages)

    memory_text = response.get("message", "") if response.get("type") == "chat" else response.get("explanation", response.get("content", ""))
    st.session_state.messages.append({"role": "assistant", "content": memory_text})
    st.session_state.display.append({"role": "assistant", "content": response})

    increment_consultations()
    store_current_session()
    st.rerun()
