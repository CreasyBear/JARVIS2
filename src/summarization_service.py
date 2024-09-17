from transformers import pipeline

class SummarizationService:
    def __init__(self):
        self.summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

    async def execute(self, text):
        try:
            summary = self.summarizer(text, max_length=130, min_length=30, do_sample=False)
            return summary[0]['summary_text']
        except Exception as e:
            return f"Error in summarization: {str(e)}"

summarization_service = SummarizationService()