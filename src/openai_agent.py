import os
from dotenv import load_dotenv
from llama_index import VectorStoreIndex, SimpleDirectoryReader, ServiceContext
from llama_index.agent import OpenAIAgent
from llama_index.tools import QueryEngineTool, ToolMetadata
from llama_index.llms import OpenAI

# Load environment variables
load_dotenv()

class EnhancedInfoRetrievalAgent:
    def __init__(self):
        self.index = self._create_index()
        self.query_engine = self.index.as_query_engine()
        self.agent = self._create_agent()

    def _create_index(self):
        documents = SimpleDirectoryReader("data").load_data()
        return VectorStoreIndex.from_documents(documents)

    def _create_agent(self):
        query_engine_tool = QueryEngineTool(
            query_engine=self.query_engine,
            metadata=ToolMetadata(
                name="knowledge_base",
                description="Useful for answering questions about the knowledge base"
            )
        )

        return OpenAIAgent.from_tools(
            [query_engine_tool],
            llm=OpenAI(model="gpt-3.5-turbo", api_key=os.getenv('OPENAI_API_KEY')),
            verbose=True
        )

    async def execute(self, task):
        return await self.agent.arun(task)