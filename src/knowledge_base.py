from llama_index import VectorStoreIndex, SimpleDirectoryReader
from llama_index.storage.storage_context import StorageContext
from llama_index.vector_stores import SimpleVectorStore
import os

class KnowledgeBase:
    def __init__(self, data_dir="data"):
        self.data_dir = data_dir
        self.index = self._create_index()

    def _create_index(self):
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)

        documents = SimpleDirectoryReader(self.data_dir).load_data()
        storage_context = StorageContext.from_defaults(vector_store=SimpleVectorStore())
        return VectorStoreIndex.from_documents(documents, storage_context=storage_context)

    def query(self, query_text):
        query_engine = self.index.as_query_engine()
        return query_engine.query(query_text)

    def update_knowledge(self):
        self.index = self._create_index()