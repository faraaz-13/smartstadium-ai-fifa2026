import os
import streamlit as st
import requests

st.set_page_config(
    page_title="SmartStadium AI — FIFA World Cup 2026",
    page_icon="🏟️",
    layout="centered"
)

st.title("🏟️ SmartStadium AI — FIFA World Cup 2026")
st.markdown("### GenAI-Powered Intelligent Stadium Operations Platform")
st.markdown("---")

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
               "model": "llama-3.3-70b-versatile",,
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

tab1, tab2 = st.tabs(["⚽ Fan Assistant", "🎛️ Staff & Operations"])

with tab1:
    st.markdown("#### Your Personal Stadium Guide 🌍")
    st.markdown("Ask anything — navigation, food, schedules, emergencies!")

    if "fan_messages" not in st.session_state:
        st.session_state.fan_messages = []

    for msg in st.session_state.fan_messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    if prompt := st.chat_input("Ask SmartStadium AI... ⚽"):
        st.session_state.fan_messages.append({
            "role": "user", "content": prompt
        })
        with st.chat_message("user"):
            st.write(prompt)
        reply = ask_ai(prompt, FAN_PROMPT)
        st.session_state.fan_messages.append({
            "role": "assistant", "content": reply
        })
        with st.chat_message("assistant"):
            st.write(reply)

with tab2:
    st.markdown("#### Operational Intelligence for Staff 🎛️")
    st.markdown("Crowd management, emergency protocols, operational support!")

    if "staff_messages" not in st.session_state:
        st.session_state.staff_messages = []

    for msg in st.session_state.staff_messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    if prompt2 := st.chat_input("Ask Operations AI... 🎛️"):
        st.session_state.staff_messages.append({
            "role": "user", "content": prompt2
        })
        with st.chat_message("user"):
            st.write(prompt2)
        reply2 = ask_ai(prompt2, STAFF_PROMPT)
        st.session_state.staff_messages.append({
            "role": "assistant", "content": reply2
        })
        with st.chat_message("assistant"):
            st.write(reply2)

st.markdown("---")
st.markdown("*Built for PromptWars 2026 | Smart Stadiums & Tournament Operations | Powered by Groq AI 🤖*")
