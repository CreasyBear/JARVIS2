import os
from datetime import datetime, timedelta
import json
import requests
from bs4 import BeautifulSoup
from github import Github
from logger import setup_logger
import arxiv

kb_logger = setup_logger('knowledge_base', 'logs/knowledge_base.log')

# You'll need to set this environment variable
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')

def download_wikipedia_article(title: str) -> str:
    """Download and extract text content from a Wikipedia article."""
    url = f"https://en.wikipedia.org/wiki/{title.replace(' ', '_')}"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    content = soup.find(id="mw-content-text").find(class_="mw-parser-output")

    return "\n\n".join(p.text for p in content.find_all('p'))

def save_article(title: str, content: str) -> None:
    """Save article content to a file."""
    os.makedirs('data', exist_ok=True)
    filename = f"data/{title.replace(' ', '_')}.txt"
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)
    kb_logger.info(f"Saved article: {filename}")

def get_github_updates(repo_name: str, days: int = 7) -> dict:
    """Fetch recent updates from a GitHub repository."""
    g = Github(GITHUB_TOKEN)
    repo = g.get_repo(repo_name)
    since = datetime.now() - timedelta(days=days)

    commits = list(repo.get_commits(since=since))
    releases = list(repo.get_releases()[:5])
    issues_and_prs = list(repo.get_issues(state='all', since=since))

    return {
        'commits': [{'sha': c.sha, 'message': c.commit.message} for c in commits],
        'releases': [{'tag': r.tag_name, 'name': r.title, 'body': r.body} for r in releases],
        'issues_and_prs': [{'number': i.number, 'title': i.title, 'body': i.body} for i in issues_and_prs]
    }

def save_github_updates(repo_name: str, updates: dict) -> None:
    """Save GitHub updates to a JSON file."""
    os.makedirs('data/github_updates', exist_ok=True)
    filename = f"data/github_updates/{repo_name.replace('/', '_')}_updates.json"
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(updates, f, indent=2)
    kb_logger.info(f"Saved GitHub updates for {repo_name}: {filename}")

def fetch_arxiv_papers(query: str, max_results: int = 5) -> list[str]:
    """Fetch recent papers from arXiv."""
    search = arxiv.Search(
        query = query,
        max_results = max_results,
        sort_by = arxiv.SortCriterion.SubmittedDate
    )
    papers = []
    for result in search.results():
        papers.append(f"Title: {result.title}\nAbstract: {result.summary}\n")
    return papers

def populate_knowledge_base() -> None:
    """Populate the knowledge base with Wikipedia articles and GitHub updates."""
    # Wikipedia articles
    topics = [
        "Artificial intelligence",
        "Machine learning",
        "Natural language processing",
        "Computer vision",
        "Robotics"
    ]

    for topic in topics:
        try:
            content = download_wikipedia_article(topic)
            save_article(topic, content)
        except Exception as e:
            kb_logger.error(f"Error downloading {topic}: {str(e)}")

    # GitHub updates
    repos = [
        "hwchase17/langchain",
        "jerryjliu/llama_index",
        "huggingface/transformers"
    ]

    for repo in repos:
        try:
            updates = get_github_updates(repo)
            save_github_updates(repo, updates)
        except Exception as e:
            kb_logger.error(f"Error fetching updates for {repo}: {str(e)}")

    # Fetch arXiv papers
    ai_papers = fetch_arxiv_papers("artificial intelligence")
    ml_papers = fetch_arxiv_papers("machine learning")

    for i, paper in enumerate(ai_papers + ml_papers):
        save_article(f"arxiv_paper_{i}", paper)

if __name__ == "__main__":
    populate_knowledge_base()