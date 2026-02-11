import requests
import xml.etree.ElementTree as ET

class SearchAgent:
    def search_papers(self, query: str, max_results: int = 5):
        """
        Search academic papers from arXiv
        """
        base_url = "http://export.arxiv.org/api/query"
        params = {
            "search_query": f"all:{query}",
            "start": 0,
            "max_results": max_results
        }

        response = requests.get(base_url, params=params)
        papers = []

        if response.status_code == 200:
            root = ET.fromstring(response.text)

            for entry in root.findall("{http://www.w3.org/2005/Atom}entry"):
                paper = {
    "title": entry.find("{http://www.w3.org/2005/Atom}title").text.strip(),
    "summary": entry.find("{http://www.w3.org/2005/Atom}summary").text.strip(),
    "link": entry.find("{http://www.w3.org/2005/Atom}id").text,
    "pdf_url": entry.find("{http://www.w3.org/2005/Atom}id").text.replace("abs", "pdf")
}
                papers.append(paper)

        return papers
