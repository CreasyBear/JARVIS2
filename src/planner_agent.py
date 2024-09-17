from llama_index.agent import OpenAIAgent
from llama_index.llms import OpenAI

class PlannerAgent:
    def __init__(self):
        self.llm = OpenAI(temperature=0, model="gpt-3.5-turbo")
        self.agent = OpenAIAgent.from_llm(self.llm)

    async def decompose_task(self, task):
        prompt = f"""
        Given the following task, break it down into a series of subtasks. For each subtask, specify:
        1. The subtask description
        2. The agent type best suited for this subtask (information, calculation, summarization, action, or web_scraping)
        3. Any prerequisite information needed for this subtask
        4. How to evaluate the correctness of the subtask result

        Task: {task}

        Respond in the following JSON format:
        {{
            "subtasks": [
                {{
                    "description": "Subtask description",
                    "agent_type": "Agent type",
                    "prerequisites": ["Prerequisite 1", "Prerequisite 2"],
                    "evaluation": "How to evaluate the result"
                }},
                ...
            ]
        }}
        """
        response = await self.agent.aquery(prompt)
        return response.response  # This will be a JSON string

planner_agent = PlannerAgent()