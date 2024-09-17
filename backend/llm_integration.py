from langchain import LLMChain
from llama_index import GPTSimpleVectorIndex
from transformers import pipeline
import logging

# Initialize logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Hugging Face pipeline
qa_pipeline = pipeline("question-answering")

# Initialize LangChain with dynamic model selection
def get_llm_chain(model_name: str):
    try:
        return LLMChain(prompt_template="Your prompt here", model=model_name)
    except Exception as e:
        logger.error(f"Error initializing LLMChain with model {model_name}: {e}")
        raise

# Initialize LlamaIndex
try:
    index = GPTSimpleVectorIndex.load_from_disk("path/to/index.json")
except Exception as e:
    logger.error(f"Error loading LlamaIndex: {e}")
    raise

def perform_qa(question, context):
    try:
        return qa_pipeline(question=question, context=context)
    except Exception as e:
        logger.error(f"Error performing QA: {e}")
        raise

def query_llama_index(query):
    try:
        response = index.query(query)
        return response
    except Exception as e:
        logger.error(f"Error querying LlamaIndex: {e}")
        raise