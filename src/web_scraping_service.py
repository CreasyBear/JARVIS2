import aiohttp
from bs4 import BeautifulSoup
from llama_index.agent import OpenAIAgent
from llama_index.llms import OpenAI

class WebScrapingService:
    def __init__(self):
        self.llm = OpenAI(temperature=0, model="gpt-3.5-turbo")
        self.openai_agent = OpenAIAgent.from_llm(self.llm)

    async def fetch_url(self, url):
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                return await response.text()

    async def extract_content(self, html):
        soup = BeautifulSoup(html, 'html.parser')
        # Remove script and style elements
        for script in soup(["script", "style"]):
            script.decompose()
        text = soup.get_text()
        # Break into lines and remove leading and trailing space on each
        lines = (line.strip() for line in text.splitlines())
        # Break multi-headlines into a line each
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        # Drop blank lines
        text = '\n'.join(chunk for chunk in chunks if chunk)
        return text

    async def summarize_content(self, content):
        summary_prompt = f"Summarize the following web content in a concise manner:\n\n{content[:4000]}"  # Limit content to 4000 chars to avoid token limits
        summary = await self.openai_agent.aquery(summary_prompt)
        return summary.response

    async def execute(self, query):
        try:
            # Extract URL from query
            url_prompt = f"Extract the URL from this query: {query}"
            url_response = await self.openai_agent.aquery(url_prompt)
            url = url_response.response.strip()

            # Fetch and extract content
            html = await self.fetch_url(url)
            content = await self.extract_content(html)

            # Summarize content
            summary = await self.summarize_content(content)

            return f"Summary of {url}:\n\n{summary}"
        except Exception as e:
            return f"Error in web scraping: {str(e)}"

web_scraping_service = WebScrapingService()