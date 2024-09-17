from transformers import pipeline
from llama_index import Document
from llama_index.node_parser import SimpleNodeParser

class SummarizationAgent:
    def __init__(self):
        self.summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
        self.node_parser = SimpleNodeParser.from_defaults()

    async def execute(self, task):
        try:
            # Assume task is in the format: "Summarize [text or file path]"
            text = task.replace("Summarize ", "").strip()

            # If it's a file path, read the file
            if text.endswith(('.txt', '.md')):
                with open(text, 'r') as file:
                    text = file.read()

            # Parse the text into nodes
            nodes = self.node_parser.get_nodes_from_documents([Document(text=text)])

            # Summarize each node
            summaries = []
            for node in nodes:
                summary = self.summarizer(node.text, max_length=130, min_length=30, do_sample=False)
                summaries.append(summary[0]['summary_text'])

            # Combine summaries
            final_summary = " ".join(summaries)

            return final_summary

        except Exception as e:
            return f"Error in summarization: {str(e)}"