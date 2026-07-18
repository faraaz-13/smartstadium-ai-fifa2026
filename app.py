import os
import anthropic
import streamlit as st

st.set_page_config(
    page_title="SmartStadium AI — FIFA World Cup 2026",
    page_icon="🏟️",
    layout="centered"
)

st.title("🏟️ SmartStadium AI — FIFA World Cup 2026")
st.markdown("### GenAI-Powered Intelligent Stadium Operations Platform")
st.markdown("---")

client = anthropic.Anthropic(
    api_key=os.environ.get("ANTHROPIC_API_KEY", "PASTE-YOUR-KEY-HERE")
)

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
- Incident response decisions
Be direct, professional, and prioritize safety."""

tab1, tab2 = st.tabs(["⚽ Fan Assistant", "🎛️ Staff & Operations"])

with tab1:
    st.markdown("#### Your Personal Stadium Guide 🌍")
    st.markdown("Ask me anything — navigation, food, schedules, emergencies!")

    if "fan_messages" not in st.session_state:
        st.session_state.fan_messages = []

    for msg in st.session_state.fan_messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    if prompt := st.chat_input("Ask SmartStadium AI... ⚽"):
        st.session_state.fan_messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.write(prompt)

        messages = [{"role": m["role"], "content": m["content"]}
                   for m in st.session_state.fan_messages]

        response = client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=300,
            system=FAN_PROMPT,
            messages=messages
        )
        reply = response.content[0].text
        st.session_state.fan_messages.append({"role": "assistant", "content": reply})
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
        st.session_state.staff_messages.append({"role": "user", "content": prompt2})
        with st.chat_message("user"):
            st.write(prompt2)

        messages2 = [{"role": m["role"], "content": m["content"]}
                    for m in st.session_state.staff_messages]

        response2 = client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=400,
            system=STAFF_PROMPT,
            messages=messages2
        )
        reply2 = response2.content[0].text
        st.session_state.staff_messages.append({"role": "assistant", "content": reply2})