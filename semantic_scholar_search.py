import requests

def search_papers(topic, year_after=2020, min_citations=50, limit=5):
    url = "https://api.semanticscholar.org/graph/v1/paper/search"

    params = {
        "query": topic,
        "limit": limit * 2,  # vi henter lidt flere og filtrerer bagefter
        "fields": "title,year,citationCount,url"
    }

    response = requests.get(url, params=params)

    if response.status_code != 200:
        print("API-fejl:", response.status_code, response.text)
        return []

    papers = response.json().get("data", [])
    filtered = [
        paper for paper in papers
        if paper.get("year", 0) > year_after and paper.get("citationCount", 0) >= min_citations
    ]

    return filtered[:limit]

if __name__ == "__main__":
    results = search_papers("artificial intelligence", year_after=2020, min_citations=50)

    for paper in results:
        print(f"📘 {paper['title']} ({paper['year']})")
        print(f"🔗 {paper['url']}")
        print(f"📈 Citations: {paper['citationCount']}\n")
