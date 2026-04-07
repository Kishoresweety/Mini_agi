from api.llm import call_llm

class ReviewerAgent:

    def review(self, text):
        prompt = f"""
        Improve and refine this output:
        {text}
        """
        return call_llm(prompt)
