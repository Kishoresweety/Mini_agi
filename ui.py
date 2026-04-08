import streamlit as st
import time

from agents.planner_agent import PlannerAgent
from agents.executor_agent import ExecutorAgent
from agents.reviewer_agent import ReviewerAgent
from memory.memory import save_memory, get_recent_context

# Initialize agents
planner = PlannerAgent()
executor = ExecutorAgent()
reviewer = ReviewerAgent()

# Page config
st.set_page_config(page_title="Lunara AI", layout="wide")

# 🎨 CUSTOM CSS (FANCY UI)
st.markdown("""
<style>

body {
    background-color: #0e1117;
    color: white;
}

.block-container {
    padding-top: 2rem;
}

/* Chat bubbles */
.user-bubble {
    background: linear-gradient(135deg, #4CAF50, #2E7D32);
    padding: 12px;
    border-radius: 12px;
    margin: 8px 0;
    color: white;
    text-align: right;
}

.ai-bubble {
    background: linear-gradient(135deg, #1f2937, #111827);
    padding: 12px;
    border-radius: 12px;
    margin: 8px 0;
    color: #e5e7eb;
}

/* Glass effect */
.glass {
    background: rgba(255, 255, 255, 0.05);
    backdrop-filter: blur(10px);
    padding: 10px;
    border-radius: 12px;
}

/* Title */
.title {
    font-size: 32px;
    font-weight: bold;
    background: linear-gradient(90deg, #00f5ff, #7c3aed);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

</style>
""", unsafe_allow_html=True)

# 🧠 Sidebar
st.sidebar.markdown("## 🧠 Memory")

if st.sidebar.button("Show Recent"):
    memory = get_recent_context()
    for m in memory:
        st.sidebar.write(m)

st.sidebar.markdown("---")
st.sidebar.write("⚡ Lunara AI v1")

# 🌟 Header
st.markdown('<div class="title">🚀 Lunara AI Agent</div>', unsafe_allow_html=True)
st.caption("Smart AI with Planning + Execution + Self-Improvement")

# Chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display messages
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f'<div class="user-bubble">{msg["content"]}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="ai-bubble">{msg["content"]}</div>', unsafe_allow_html=True)

# Input
user_input = st.chat_input("Type your message...")

if user_input:

    # Save user message
    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })

    st.markdown(f'<div class="user-bubble">{user_input}</div>', unsafe_allow_html=True)

    with st.spinner("🧠 Thinking..."):

        context = get_recent_context()

        # Plan
        steps = planner.plan(user_input)

        # Fancy thinking panel
        with st.expander("🧠 Agent Thinking"):
            st.markdown('<div class="glass">', unsafe_allow_html=True)
            for i, step in enumerate(steps, 1):
                st.write(f"🔹 {step}")
            st.markdown('</div>', unsafe_allow_html=True)

        # Execution
        result = user_input

        with st.expander("⚙️ Execution Flow"):
            st.markdown('<div class="glass">', unsafe_allow_html=True)

            for i, step in enumerate(steps, 1):
                st.write(f"➡️ Step {i}: {step}")
                result = executor.execute(step, result)
                st.success(result)

            st.markdown('</div>', unsafe_allow_html=True)

        # Review
        with st.expander("🔍 Review Stage"):
            st.markdown('<div class="glass">Refining output...</div>', unsafe_allow_html=True)

        final_output = reviewer.review(result)

        # Save memory
        save_memory({
            "input": user_input,
            "steps": steps,
            "output": final_output
        })

        # Streaming output
        placeholder = st.empty()
        full_text = ""

        for word in final_output.split():
            full_text += word + " "
            placeholder.markdown(f'<div class="ai-bubble">{full_text}</div>', unsafe_allow_html=True)
            time.sleep(0.02)

    # Save AI response
    st.session_state.messages.append({
        "role": "assistant",
        "content": final_output
    })
