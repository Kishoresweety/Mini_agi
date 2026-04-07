from api.llm import call_llm

class PlannerAgent:

    def plan(self, user_input):
        prompt = f"""
        Break this into steps:
        {user_input}

        Available steps:
        - summarize
        - improve

        Return steps like:
        1. summarize
        2. improve
        """

        response = call_llm(prompt)

        steps = []
        for line in response.split("\n"):
            if "." in line:
                steps.append(line.split(".", 1)[1].strip().lower())

        return steps
