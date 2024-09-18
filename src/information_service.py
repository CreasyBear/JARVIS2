from llama_index import VectorStoreIndex, SimpleDirectoryReader, ServiceContext
from llama_index.llms import OpenAI
from llama_index.embeddings import OpenAIEmbedding
from llama_index.node_parser import SimpleNodeParser
from llama_index.agent import OpenAIAgent
from llama_index.tools import QueryEngineTool, ToolMetadata
import os
from backend.cache import get_cached_data, set_cached_data
import logging

class InformationService:
    def __init__(self):
        self.llm = OpenAI(temperature=0, model="gpt-3.5-turbo")
        self.embed_model = OpenAIEmbedding()
        self.node_parser = SimpleNodeParser.from_defaults()
        self.service_context = ServiceContext.from_defaults(llm=self.llm, embed_model=self.embed_model, node_parser=self.node_parser)
        self.knowledge_base = self._create_knowledge_base()
        self.query_engine = self.knowledge_base.as_query_engine()
        self.openai_agent = self._create_openai_agent()
        self.logger = logging.getLogger('information')
        self.logger.setLevel(logging.INFO)

    def _create_knowledge_base(self):
        data_dir = os.getenv('DATA_DIR', 'data')
        if not os.path.exists(data_dir):
            os.makedirs(data_dir)
        documents = SimpleDirectoryReader(data_dir).load_data()
        return VectorStoreIndex.from_documents(documents, service_context=self.service_context)

    def _create_openai_agent(self):
        query_engine_tool = QueryEngineTool(
            query_engine=self.query_engine,
            metadata=ToolMetadata(
                name="knowledge_base",
                description="Useful for answering questions about the knowledge base"
            )
        )
        return OpenAIAgent.from_tools([query_engine_tool], llm=self.llm)

    async def execute(self, query):
        self.logger.info(f"Received query: {query}")
        try:
            cached_response = get_cached_data(query)
            if cached_response:
                self.logger.info("Returning cached response.")
                return cached_response.decode('utf-8')

            response = self.openai_agent.run(query)
            set_cached_data(query, response)
            self.logger.info("Query executed successfully.")
            return response
        except Exception as e:
            self.logger.error(f"Error executing query: {e}", exc_info=True)
            raise

# Removed InformationRetrievalService as it's consolidated into InformationService

information_service = InformationService()