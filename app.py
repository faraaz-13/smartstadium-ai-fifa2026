import os
import streamlit as st
import requests

st.set_page_config(
    page_title="SmartStadium AI — FIFA World Cup 2026",
    page_icon="🏟️",
    layout="wide"
)

st.markdown("""
<style>
    .stApp { background: #08080f; color: white; }
    .main { padding: 0 2rem; }
    .hero-box {
        background: linear-gradient(135deg, #0a0a1a 0%, #1a0a2e 50%, #0a1a3e 100%);
        border-radius: 20px; padding: 48px 32px;
        text-align: center; margin-bottom: 24px;
        border: 1px solid rgba(255,255,255,0.1);
    }
    .hero-title { font-size: 42px; font-weight: 700; color: white; margin-bottom: 8px; }
    .hero-sub { font-size: 18px; color: rgba(255,255,255,0.6); margin-bottom: 24px; }
    .badge {
        display: inline-block; background: rgba(0,229,255,0.1);
        border: 1px solid rgba(0,229,255,0.3); border-radius: 50px;
        padding: 6px 18px; font-size: 13px; color: #00e5ff; margin-bottom: 20px;
    }
    .stat-box {
        background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.1);
        border-radius: 16px; padding: 20px; text-align: center;
    }
    .stat-num { font-size: 28px; font-weight: 700; color: #a855f7; }
    .stat-label { font-size: 13px; color: rgba(255,255,255,0.5); margin-top: 4px; }
    .feat-box {
        background: rgba(255,255,255,0.04); border: 1px solid rgba(255,255,255,0.08);
        border-radius: 16px; padding: 20px; height: 100%;
    }
    .feat-title { font-size: 16px; font-weight: 600; color: white; margin: 8px 0 4px; }
    .feat-desc { font-size: 13px; color: rgba(255,255,255,0.5); line-height: 1.6; }
    .stChatMessage { background: rgba(255,255,255,0.05) !important; border-radius: 12px !important; }
    .stChatInputContainer { background: rgba(255,255,255,0.05) !important; border-radius: 16px !important; }
    .stTabs [data-baseweb="tab-list"] { background: rgba(255,255,255,0.05); border-radius: 12px; }
    .stTabs [data-baseweb="tab"] { color: rgba(255,255,255,0.6) !important; }
    .stTabs [aria-selected="true"] { color: #a855f7 !important; }
    div[data-testid="stMetric"] {
        background: rgba(255,255,255,0.05);
        border: 1px solid rgba(255,255,255,0.1);
        border-radius: 12px; padding: 16px;
    }
    .footer {
        text-align: center; padding: 20px;
        color: rgba(255,255,255,0.3); font-size: 13px;
        border-top: 1px solid rgba(255,255,255,0.1);
        margin-top: 32px;
    }
    .stButton > button {
        background: linear-gradient(135deg, #7c3aed, #2563eb) !important;
        color: white !important; border: none !important;
        border-radius: 50px !important; padding: 12px 28px !important;
    }
    h1,h2,h3 { color: white !important; }
    p { color: rgba(255,255,255,0.7) !important; }
</style>
""", unsafe_allow_html=True)

API_KEY = st.secrets["GROQ_API_KEY"]

FAN_PROMPT = """You are SmartStadium AI — official FIFA World Cup 2026
stadium assistant. Help fans with:
- Seat navigation (Sections A-Z, Gates 1-10)
- Food courts (Halal: Gates 2,4,7 | Veg: Gates 1,5,9)
- Match schedules and player stats
- Restrooms, medical, parking, transport
- Emergency: always say call +1-800-FIFA-HELP
- Accessibility: wheelchair routes via Gates 1,5
Reply in the same language the fan writes in.
Be friendly and answer in max 3 sentences."""

STAFF_PROMPT = """You are SmartStadium OPS — FIFA World Cup 2026
operations AI for staff, organizers and volunteers. Help with:
- Crowd management and congestion alerts
- Emergency evacuation protocols
- Volunteer deployment suggestions
- Sustainability and waste management
Be direct, professional, and prioritize safety."""

def ask_ai(prompt, system):
    try:
        response = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "llama-3.3-70b-versatile",
                "messages": [
                    {"role": "system", "content": system},
                    {"role": "user", "content": prompt}
                ],
                "max_tokens": 300
            }
        )
        data = response.json()
        if "choices" in data:
            return data["choices"][0]["message"]["content"]
        else:
            return f"Error: {data}"
    except Exception as e:
        return f"Error: {str(e)}"

st.markdown("""
<div class="hero-box">
    <div class="badge">🟢 Live — FIFA World Cup 2026</div>
    <div class="hero-title">🏟️ SmartStadium AI</div>
    <div class="hero-sub">GenAI-powered assistant for fans, staff and organizers</div>
    <div style="display:flex;gap:10px;justify-content:center;flex-wrap:wrap;">
        <span style="background:rgba(168,85,247,0.2);border:1px solid rgba(168,85,247,0.4);border-radius:50px;padding:5px 14px;font-size:12px;color:#a855f7">⚽ Seat navigation</span>
        <span style="background:rgba(0,229,255,0.1);border:1px solid rgba(0,229,255,0.3);border-radius:50px;padding:5px 14px;font-size:12px;color:#00e5ff">🍕 Food courts</span>
        <span style="background:rgba(255,45,120,0.1);border:1px solid rgba(255,45,120,0.3);border-radius:50px;padding:5px 14px;font-size:12px;color:#ff2d78">🚨 Emergency help</span>
        <span style="background:rgba(0,255,157,0.1);border:1px solid rgba(0,255,157,0.3);border-radius:50px;padding:5px 14px;font-size:12px;color:#00ff9d">🌍 Multilingual</span>
        <span style="background:rgba(255,230,0,0.1);border:1px solid rgba(255,230,0,0.3);border-radius:50px;padding:5px 14px;font-size:12px;color:#ffe600">🎛️ Staff ops</span>
    </div>
</div>
""", unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown('<div class="stat-box"><div class="stat-num">50K+</div><div class="stat-label">Fans served</div></div>', unsafe_allow_html=True)
with col2:
    st.markdown('<div class="stat-box"><div class="stat-num">8</div><div class="stat-label">Problem areas covered</div></div>', unsafe_allow_html=True)
with col3:
    st.markdown('<div class="stat-box"><div class="stat-num">&lt;1s</div><div class="stat-label">Response time</div></div>', unsafe_allow_html=True)
with col4:
    st.markdown('<div class="stat-box"><div class="stat-num">20+</div><div class="stat-label">Languages</div></div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

tab1, tab2 = st.tabs(["⚽ Fan Assistant", "🎛️ Staff & Operations"])

with tab1:
    st.markdown("#### Your personal stadium guide 🌍")
    st.markdown("Ask anything — navigation, food, schedules, emergencies!")

    col_ex1, col_ex2, col_ex3, col_ex4 = st.columns(4)
    with col_ex1:
        if st.button("📍 Where is Section B?"):
            st.session_state.fan_quick = "Where is Section B Row 12 Seat 5?"
    with col_ex2:
        if st.button("🍖 Halal food near Gate 4?"):
            st.session_state.fan_quick = "What halal food is near Gate 4?"
    with col_ex3:
        if st.button("⚽ Brazil match time?"):
            st.session_state.fan_quick = "When does Brazil play today?"
    with col_ex4:
        if st.button("🚨 Lost child help"):
            st.session_state.fan_quick = "My child is lost please help!"

    if "fan_messages" not in st.session_state:
        st.session_state.fan_messages = []
    if "fan_quick" in st.session_state:
        q = st.session_state.pop("fan_quick")
        st.session_state.fan_messages.append({"role": "user", "content": q})
        reply = ask_ai(q, FAN_PROMPT)
        st.session_state.fan_messages.append({"role": "assistant", "content": reply})

    for msg in st.session_state.fan_messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    if prompt := st.chat_input("Ask SmartStadium AI... ⚽"):
        st.session_state.fan_messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.write(prompt)
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                reply = ask_ai(prompt, FAN_PROMPT)
            st.write(reply)
        st.session_state.fan_messages.append({"role": "assistant", "content": reply})

with tab2:
    st.markdown("#### Operational intelligence for staff 🎛️")

    col_s1, col_s2, col_s3 = st.columns(3)
    with col_s1:
        if st.button("🚨 Gate 3 congested"):
            st.session_state.staff_quick = "Gate 3 is heavily congested what should I do?"
    with col_s2:
        if st.button("🏥 Fan fainted"):
            st.session_state.staff_quick = "A fan fainted in Section C what are next steps?"
    with col_s3:
        if st.button("📋 Half-time plan"):
            st.session_state.staff_quick = "Give me the half-time crowd management plan"

    if "staff_messages" not in st.session_state:
        st.session_state.staff_messages = []
    if "staff_quick" in st.session_state:
        q = st.session_state.pop("staff_quick")
        st.session_state.staff_messages.append({"role": "user", "content": q})
        reply = ask_ai(q, STAFF_PROMPT)
        st.session_state.staff_messages.append({"role": "assistant", "content": reply})

    for msg in st.session_state.staff_messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    if prompt2 := st.chat_input("Ask Operations AI... 🎛️"):
        st.session_state.staff_messages.append({"role": "user", "content": prompt2})
        with st.chat_message("user"):
            st.write(prompt2)
        with st.chat_message("assistant"):
            with st.spinner("Processing..."):
                reply2 = ask_ai(prompt2, STAFF_PROMPT)
            st.write(reply2)
        st.session_state.staff_messages.append({"role": "assistant", "content": reply2})

st.markdown("<br>", unsafe_allow_html=True)
st.markdown("#### Why SmartStadium AI?")
col_f1, col_f2, col_f3, col_f4 = st.columns(4)
with col_f1:
    st.markdown('<div class="feat-box"><div style="font-size:28px">🗺️</div><div class="feat-title">Smart navigation</div><div class="feat-desc">Real-time seat directions and gate info for 50,000+ fans</div></div>', unsafe_allow_html=True)
with col_f2:
    st.markdown('<div class="feat-box"><div style="font-size:28px">🌍</div><div class="feat-title">Multilingual</div><div class="feat-desc">Auto-detects your language — Arabic, Spanish, Hindi and more</div></div>', unsafe_allow_html=True)
with col_f3:
    st.markdown('<div class="feat-box"><div style="font-size:28px">🎛️</div><div class="feat-title">Staff intelligence</div><div class="feat-desc">Crowd alerts, emergency protocols and operational support</div></div>', unsafe_allow_html=True)
with col_f4:
    st.markdown('<div class="feat-box"><div style="font-size:28px">🚨</div><div class="feat-title">Emergency ready</div><div class="feat-desc">Instant safety guidance and evacuation route assistance</div></div>', unsafe_allow_html=True)

st.markdown("""
<div class="footer">
    Built for PromptWars Hackathon 2026 · Smart Stadiums & Tournament Operations · Powered by Groq AI 🤖
    <br>Team DWITARA · Vemu Institute of Technology · Chittoor, AP
</div>
""", unsafe_allow_html=True)
