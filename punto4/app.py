# app.py
# Streamlit UI — Insights ACH Funding Agent

import streamlit as st
from agent import create_agent, send_message
from memory import get_client_memory, save_client_memory

# ── Page config ───────────────────────────────────────────────────
st.set_page_config(
    page_title="Insights — ACH Funding Agent",
    page_icon="💼",
    layout="centered"
)

st.title("💼 Insights Wealth Management")
st.caption("ACH Funding Assistant — Powered by Sofia")

# ── Session state init ────────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = []

if "chat_session" not in st.session_state:
    api_key = st.secrets["GEMINI_API_KEY"]
    st.session_state.chat_session = create_agent(api_key)

if "client_id" not in st.session_state:
    st.session_state.client_id = None

if "session_complete" not in st.session_state:
    st.session_state.session_complete = False

# ── Sidebar ───────────────────────────────────────────────────────
with st.sidebar:
    st.header("⚙️ Demo Controls")
    st.caption("Use these controls to simulate ACH outcomes")

    sim_result = st.selectbox(
        "Simulate transaction result:",
        ["✅ Success", "⚠️ R01 — Insufficient Funds", "❌ R03 — Account Not Found"]
    )

    st.divider()
    client_id = st.text_input("Client ID (for memory)", value="C001")
    if st.button("Load client memory"):
        memory = get_client_memory(client_id)
        if memory:
            st.success(f"Memory found: {memory['bank'].title()} in {memory['state'].title()}")
            st.session_state.client_id = client_id
        else:
            st.info("No memory found for this client.")

    if st.button("Save session memory"):
        if st.session_state.client_id:
            save_client_memory(
                client_id=st.session_state.client_id,
                bank=st.session_state.get("bank", "unknown"),
                state=st.session_state.get("state", "unknown"),
                account_type=st.session_state.get("account_type", "checking")
            )
            st.success("Memory saved.")

    st.divider()
    if st.button("🔄 Reset conversation"):
        st.session_state.messages = []
        api_key = st.secrets["GEMINI_API_KEY"]
        st.session_state.chat_session = create_agent(api_key)
        st.session_state.session_complete = False
        st.rerun()

# ── Chat history display ──────────────────────────────────────────
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ── Initial greeting ──────────────────────────────────────────────
if not st.session_state.messages:
    memory = get_client_memory(client_id) if client_id else None
    if memory:
        greeting = (
            f"Welcome back to Insights! I see you previously funded using "
            f"**{memory['bank'].title()}** in **{memory['state'].title()}**. "
            f"Would you like to use the same account, or set up a new one?"
        )
    else:
        greeting = (
            "Welcome to Insights Wealth Management! I'm Sofia, your funding assistant. "
            "I'm here to help you fund your investment account via ACH bank transfer. "
            "How can I help you today?"
        )
    st.session_state.messages.append({"role": "assistant", "content": greeting})
    with st.chat_message("assistant"):
        st.markdown(greeting)

# ── User input ────────────────────────────────────────────────────
if prompt := st.chat_input("Type your message here..."):
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Check if this is a confirmation step and inject simulation result
    confirmation_keywords = ["confirm", "yes", "correct", "proceed", "looks good"]
    is_confirmation = any(word in prompt.lower() for word in confirmation_keywords)

    if is_confirmation and sim_result != "✅ Success":
        if "R01" in sim_result:
            injected = (
                prompt + "\n\n[SYSTEM: Transaction attempted. "
                "Result: R01 — Insufficient Funds. Handle accordingly.]"
            )
        else:
            injected = (
                prompt + "\n\n[SYSTEM: Transaction attempted. "
                "Result: R03 — No Account / Unable to Locate. Handle accordingly.]"
            )
        response = send_message(st.session_state.chat_session, injected)
    else:
        response = send_message(st.session_state.chat_session, prompt)

    # Add assistant response
    st.session_state.messages.append({"role": "assistant", "content": response})
    with st.chat_message("assistant"):
        st.markdown(response)
```

---

**`requirements.txt`**
```
streamlit>=1.32.0
google-generativeai>=0.5.0
