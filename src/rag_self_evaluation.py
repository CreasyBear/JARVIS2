import os
import json
from typing import List
from llama_index import VectorStoreIndex, SimpleDirectoryReader, Document
from llama_index.evaluation import DatasetGenerator, QueryResponseEvaluator
from logger import setup_logger

rag_logger = setup_logger('rag', 'logs/rag.log')

def load_github_updates() -> List[Document]:
    """Load GitHub updates from JSON files and convert them to Documents."""
    updates_dir = 'data/github_updates'
    documents = []
    for filename in os.listdir(updates_dir):
        if filename.endswith('_updates.json'):
            with open(os.path.join(updates_dir, filename), 'r') as f:
                data = json.load(f)
                repo_name = filename.replace('_updates.json', '').replace('_', '/')
                content = f"Updates for {repo_name}:\n\n"

                content += "Recent commits:\n"
                content += "\n".join(f"- {commit['message']}" for commit in data['commits'])

                content += "\n\nRecent releases:\n"
                for release in data['releases']:
                    content += f"- {release['tag']}: {release['name']}\n{release['body']}\n\n"

                content += "Recent issues and pull requests:\n"
                content += "\n".join(f"- #{issue['number']}: {issue['title']}\n{issue['body']}" for issue in data['issues_and_prs'])

                documents.append(Document(text=content))
    return documents

def run_rag_evaluation() -> None:
    """Run the RAG evaluation process."""
    rag_logger.info("Loading documents...")
    wiki_documents = SimpleDirectoryReader('data').load_data()
    github_documents = load_github_updates()
    all_documents = wiki_documents + github_documents

    index = VectorStoreIndex.from_documents(all_documents)

    rag_logger.info("Generating evaluation dataset...")
    dataset_generator = DatasetGenerator.from_documents(all_documents)
    eval_dataset = dataset_generator.generate_dataset(num_questions=10)

    rag_logger.info("Running evaluation...")
    query_engine = index.as_query_engine()
    evaluator = QueryResponseEvaluator()

    total_score = 0
    for i, example in enumerate(eval_dataset):
        query = example.query
        response = query_engine.query(query)
        eval_result = evaluator.evaluate(query, response, example.relevant_docs)
        total_score += eval_result.score
        rag_logger.info(f"Query {i+1}: {query}")
        rag_logger.info(f"Evaluation score: {eval_result.score}")

    average_score = total_score / len(eval_dataset)
    rag_logger.info(f"Average evaluation score: {average_score}")

if __name__ == "__main__":
    run_rag_evaluation()