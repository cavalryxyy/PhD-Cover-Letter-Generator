# FILE: 03_supervisor_analysis/step3_web_searcher.py
# PURPOSE: Web searcher for supervisor analysis.

import requests
import logging
from bs4 import BeautifulSoup

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class WebSearcher:
    """
    Searches the web for supervisor information.
    """
    def __init__(self):
        """
        Initializes the web searcher.
        """
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })

    def search(self, professor_name: str, university: str, publication_url: str) -> list[str]:
        """
        Searches for the supervisor's research domains.
        """
        logger.info(f"Searching for research domains of {professor_name} at {university}")
        
        try:
            response = self.session.get(publication_url, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            text = soup.get_text().lower()
            
            research_keywords = [
                "human-computer interaction", "hci", "machine learning", "artificial intelligence",
                "computer vision", "natural language processing", "robotics", "data science",
                "software engineering", "human-ai interaction", "mixed reality", "virtual reality",
                "autonomous vehicles", "internet of things", "cybersecurity", "blockchain",
                "deep learning", "neural networks", "computer graphics", "user experience",
                "interaction design", "accessibility", "ubiquitous computing"
            ]
            
            found_areas = [keyword for keyword in research_keywords if keyword in text]
            
            return list(set(found_areas))
            
        except Exception as e:
            logger.error(f"Failed to scrape publication page {publication_url}: {e}")
            return []
