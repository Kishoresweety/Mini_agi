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
st.set_page_config(page_title="Mini AI Agent", layout="wide")

st.title("🤖 Mini AI Agent (Lunara Prototype)")

# Chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Input
user_input = st.chat_input("Type your message...")

if user_input:

    # Show user message
    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })

    with st.chat_message("user"):
        st.markdown(user_input)

    # AI Response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):

            # Memory
            context = get_recent_context()

            # Plan
            steps = planner.plan(user_input)

            # 🧠 Thinking Panel
            with st.expander("🧠 Agent Thinking"):
                st.subheader("Plan")
                for i, step in enumerate(steps, 1):
                    st.write(f"{i}. {step}")

            # ⚙️ Execution
            result = user_input

            with st.expander("⚙️ Execution Steps"):
                for i, step in enumerate(steps, 1):
                    st.write(f"➡️ Step {i}: {step}")

                    result = executor.execute(step, result)

                    st.success(f"Output after step {i}:")
                    st.write(result)

            # 🔍 Review
            with st.expander("🔍 Review Stage"):
                st.write("Refining final output...")

            final_output = reviewer.review(result)

            # Save memory
            save_memory({
                "input": user_input,
                "steps": steps,
                "output": final_output
            })

            # 🚀 Streaming Output
            placeholder = st.empty()
            full_text = ""

            for word in final_output.split():
                full_text += word + " "
                placeholder.markdown(full_text)
                time.sleep(0.02)

    # Save AI response
    st.session_state.messages.append({
        "role": "assistant",
        "content": final_output
    })
