import streamlit as st
from agent import create_agent, start_chat, send_message
from memory import get_client_memory, save_client_memory

# ── Page config ───────────────────────────────────────────────────
st.set_page_config(
    page_title="Insights WM — Sofia",
    page_icon="💼",
    layout="centered"
)

# ── Custom CSS — Insights Visual Identity ─────────────────────────
st.markdown("""
<style>
/* Global */
html, body, [class*="css"] {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    color: #1A1A1A;
    background-color: #FFFFFF;
}

#MainMenu, footer, header {visibility: hidden;}

.block-container {
    max-width: 820px;
    padding-top: 1.5rem;
    padding-bottom: 2rem;
}

/* Chat messages */
.stChatMessage {
    border-radius: 2px !important;
    border: 1px solid #E1E8ED !important;
    box-shadow: 0 1px 3px rgba(0,0,0,0.04) !important;
    margin-bottom: 6px !important;
}

/* User message */
.stChatMessage[data-testid="chat-message-user"] {
    background-color: #F4F7F9 !important;
    border-left: 3px solid #002D62 !important;
}

/* Assistant message */
.stChatMessage[data-testid="chat-message-assistant"] {
    background-color: #FFFFFF !important;
    border-left: 3px solid #C5A059 !important;
}

/* Chat input */
.stChatInput textarea {
    border: 1px solid #E1E8ED !important;
    border-radius: 2px !important;
    font-size: 0.9rem !important;
    line-height: 1.6 !important;
}
.stChatInput textarea:focus {
    border-color: #002D62 !important;
    box-shadow: none !important;
}

/* Buttons */
.stButton > button {
    background-color: #002D62 !important;
    color: #FFFFFF !important;
    border: none !important;
    border-radius: 2px !important;
    font-size: 0.82rem !important;
    font-weight: 600 !important;
    padding: 0.45rem 1rem !important;
    transition: background-color 0.3s ease !important;
    width: 100%;
}
.stButton > button:hover {
    background-color: #003d82 !important;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background-color: #F4F7F9 !important;
    border-right: 1px solid #E1E8ED !important;
}

/* Inputs */
.stSelectbox > div > div,
.stTextInput > div > input {
    border: 1px solid #E1E8ED !important;
    border-radius: 2px !important;
    font-size: 0.88rem !important;
}

hr {
    border: none !important;
    border-top: 1px solid #E1E8ED !important;
    margin: 12px 0 !important;
}
</style>
""", unsafe_allow_html=True)

# ── Header with logo ──────────────────────────────────────────────
col1, col2 = st.columns([1, 3])
with col1:
    try:
        st.image("punto4/Logoprueba.png", width=140)
    except Exception:
        st.markdown("**INSIGHTS**")
with col2:
    st.markdown("""
    <div style="padding-top: 12px;">
        <p style="font-family: 'Playfair Display', serif; font-size: 1.3rem;
           font-weight: 700; color: #002D62; margin: 0; letter-spacing: -0.02em;">
           ACH Funding Assistant
        </p>
        <p style="font-family: 'Montserrat', sans-serif; font-size: 0.72rem;
           color: #C5A059; margin: 2px 0 0 0; letter-spacing: 0.08em;
           text-transform: uppercase;">
           Powered by Sofia · Wealth Management
        </p>
    </div>
    """, unsafe_allow_html=True)

st.markdown(
    "<div style='border-bottom: 2px solid #C5A059; margin-bottom: 24px;'></div>",
    unsafe_allow_html=True
)

# ── Session state init ────────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = []

if "chat_session" not in st.session_state:
    api_key = st.secrets["GEMINI_API_KEY"]
    client = create_agent(api_key)
    st.session_state.chat_session = start_chat(client)

if "client_id" not in st.session_state:
    st.session_state.client_id = None

if "session_complete" not in st.session_state:
    st.session_state.session_complete = False

if "summary_shown" not in st.session_state:
    st.session_state.summary_shown = False

# ── Sidebar ───────────────────────────────────────────────────────
with st.sidebar:
    try:
        st.image("punto4/Logoprueba.png", width=120)
    except Exception:
        st.markdown("**INSIGHTS WM**")

    st.markdown("---")
    st.markdown("### Demo Controls")
    st.caption("Simulate ACH transaction outcomes")

    sim_result = st.selectbox(
        "Transaction result:",
        ["✅ Success", "⚠️ R01 — Insufficient Funds", "❌ R03 — Account Not Found"]
    )

    st.markdown("---")
    st.markdown("### Client Memory")

    client_id = st.text_input("Client ID", value="C001")

    if st.button("Load Memory"):
        memory = get_client_memory(client_id)
        if memory:
            st.success(
                f"**{memory['bank'].title()}** · {memory['state'].title()}\n\n"
                f"Type: {memory['account_type']} · "
                f"Last funded: {memory['last_funded_at'][:10]}"
            )
            st.session_state.client_id    = client_id
            st.session_state.bank         = memory["bank"]
            st.session_state.state        = memory["state"]
            st.session_state.account_type = memory["account_type"]
        else:
            st.info("No memory found for this client.")

    st.caption("Save after a completed session:")
    manual_bank  = st.text_input("Bank", value=st.session_state.get("bank", ""))
    manual_state = st.text_input("State", value=st.session_state.get("state", ""))
    manual_type  = st.selectbox("Account type", ["checking", "savings"])

    if st.button("Save Memory"):
        if client_id and manual_bank and manual_state:
            save_client_memory(
                client_id    = client_id,
                bank         = manual_bank,
                state        = manual_state,
                account_type = manual_type
            )
            st.session_state.client_id    = client_id
            st.session_state.bank         = manual_bank
            st.session_state.state        = manual_state
            st.session_state.account_type = manual_type
            st.success(f"Memory saved for **{client_id}**.")
        else:
            st.warning("Fill in Client ID, Bank, and State.")

    st.markdown("---")
    if st.button("🔄 Reset Conversation"):
        st.session_state.messages = []
        api_key = st.secrets["GEMINI_API_KEY"]
        client = create_agent(api_key)
        st.session_state.chat_session = start_chat(client)
        st.session_state.session_complete = False
        st.session_state.summary_shown = False
        st.rerun()

    st.markdown("---")
    st.markdown(
        "<p style='font-size:0.7rem; color:#4A4A4A; line-height:1.6;'>"
        "Este agente es un prototipo de demostración.<br>"
        "No procesa transacciones reales.</p>",
        unsafe_allow_html=True
    )

# ── Chat history display ──────────────────────────────────────────
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ── Initial greeting ──────────────────────────────────────────────
if not st.session_state.messages:
    memory = get_client_memory(client_id) if client_id else None
    if memory:
        # Inyectar memoria en el historial de Gemini ANTES del greeting
        memory_injection = (
            f"[SYSTEM CONTEXT — NOT VISIBLE TO CLIENT: "
            f"This client has previous session data. "
            f"Bank: {memory['bank'].title()}, "
            f"State: {memory['state'].title()}, "
            f"Account type: {memory['account_type']}. "
            f"Last funded: {memory['last_funded_at'][:10]}. "
            f"You already know their bank and state. "
            f"Do NOT ask for bank and state again unless they want a new account. "
            f"Greet them as a returning client and confirm if they want to use "
            f"the same account.]"
        )
        send_message(st.session_state.chat_session, memory_injection)

        greeting = (
            f"Bienvenido de nuevo a Insights Wealth Management. "
            f"Veo que anteriormente fondeaste usando "
            f"**{memory['bank'].title()}** en **{memory['state'].title()}**. "
            f"¿Deseas usar la misma cuenta o configurar una nueva?"
        )
    else:
        greeting = (
            "Bienvenido a Insights Wealth Management. Soy Sofia, "
            "tu asistente de fondeo. Estoy aquí para ayudarte a "
            "depositar fondos en tu cuenta de inversión vía transferencia ACH. "
            "¿En qué puedo ayudarte hoy?"
        )

    # El greeting va al historial visual pero NO al historial de Gemini
    # para evitar que aparezca como mensaje de usuario
    st.session_state.messages.append({"role": "assistant", "content": greeting})
    with st.chat_message("assistant"):
        st.markdown(greeting)

# ── User input ────────────────────────────────────────────────────
if prompt := st.chat_input("Escribe tu mensaje aquí..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    confirmation_keywords = [
        "confirmo", "sí", "si", "correcto", "adelante", "procede",
        "confirm", "yes", "correct", "proceed", "looks good",
        "sip", "dale", "listo", "ok", "okay", "autorizo"
    ]

    summary_keywords = [
        "resumen", "summary", "aquí tienes un resumen",
        "here is a summary", "before we proceed",
        "antes de proceder", "todo correcto",
        "everything correct", "confirma los detalles",
        "please confirm", "por favor confirma"
    ]

    is_confirmation = any(
        word in prompt.lower() for word in confirmation_keywords
    )

    # Revisar si el último mensaje de Sofia fue el resumen final
    last_assistant_message = ""
    for msg in reversed(st.session_state.messages):
        if msg["role"] == "assistant":
            last_assistant_message = msg["content"].lower()
            break

    summary_just_shown = any(
        keyword in last_assistant_message
        for keyword in summary_keywords
    )

    if summary_just_shown:
        st.session_state.summary_shown = True

    if is_confirmation and st.session_state.summary_shown and sim_result != "✅ Success":
        if "R01" in sim_result:
            injected = (
                prompt + "\n\n[SYSTEM: Transaction attempted. "
                "Result: R01 — Insufficient Funds. Handle accordingly "
                "in the same language the client is using.]"
            )
        else:
            injected = (
                prompt + "\n\n[SYSTEM: Transaction attempted. "
                "Result: R03 — No Account / Unable to Locate. Handle accordingly "
                "in the same language the client is using.]"
            )
        response = send_message(st.session_state.chat_session, injected)
        st.session_state.summary_shown = False
    else:
        response = send_message(st.session_state.chat_session, prompt)

    st.session_state.messages.append({"role": "assistant", "content": response})
    with st.chat_message("assistant"):
        st.markdown(response)
