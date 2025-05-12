import requests
from typing import List, Dict

def search_papers(topic: str, year_condition: str = 'after', year: int = 2020, min_citations: int = 50, limit: int = 5) -> List[Dict]:
    
    url = "https://api.semanticscholar.org/graph/v1/paper/search"

    op_map = {'before': '<', 'after': '>', 'equal to': '='}
    year_operator = op_map.get(year_condition, '>')

    params = {
        "query": topic,
        "limit": limit * 2,  # vi henter lidt flere og filtrerer bagefter
        "fields": "title,year,citationCount,url"
    }

    resp = requests.get(url, params=params)

    if resp.status_code != 200:
        print("API-fejl:", resp.status_code, resp.text)
        return []

    papers = resp.json().get("data", [])
    filtered = [
        p for p in papers
            if (
        (year_operator == '>' and p.get("year", 0) > year) or
        (year_operator == '<' and p.get("year", 0) < year) or
        (year_operator == '=' and p.get("year", 0) == year)
        )
        and p.get("citationCount", 0) >= min_citations
    ]

    return filtered[:limit]

