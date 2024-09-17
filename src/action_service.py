from llama_index.llms import OpenAI
from llama_index.agent import OpenAIAgent

class ActionService:
    def __init__(self):
        self.llm = OpenAI(temperature=0, model="gpt-3.5-turbo")
        self.openai_agent = OpenAIAgent.from_llm(self.llm)

    async def execute(self, query):
        action_prompt = f"Describe the steps to perform this action: {query}"
        response = await self.openai_agent.aquery(action_prompt)
        return response.response

action_service = ActionService()