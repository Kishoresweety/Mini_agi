from groq import Groq
from openai import OpenAI
import streamlit as st

provider = st.secrets["LLM_PROVIDER"]

def call_llm(prompt):

    if provider == "groq":
        client = Groq(api_key=st.secrets["GROQ_API_KEY"])
        response = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="openai/gpt-oss-120b"
        )
        return response.choices[0].message.content

    elif provider == "openai":
        client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
        response = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="gpt-4o-mini"
        )
        return response.choices[0].message.content
