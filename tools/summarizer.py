from api.llm import call_llm

def summarize(text):
    prompt = f"Summarize this:\n{text}"
    return call_llm(prompt)
