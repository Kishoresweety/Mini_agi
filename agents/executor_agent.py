from tools.summarizer import summarize
from tools.improver import improve

class ExecutorAgent:

    def execute(self, step, text):
        if "summarize" in step:
            return summarize(text)

        elif "improve" in step:
            return improve(text)

        return text
