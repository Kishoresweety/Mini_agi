from api.llm import call_llm

def improve(text):
    prompt = f"Improve this text:\n{text}"
    return call_llm(prompt)
