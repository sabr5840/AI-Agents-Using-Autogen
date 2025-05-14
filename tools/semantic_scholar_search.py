import requests
from typing import List, Dict

def search_papers(topic: str, year_condition: str = 'after', year: int = 2020, min_citations: int = 50, limit: int = 5) -> List[Dict]:
    
    dummy_data = [
    {
        "title": "Attention Is All You Need",
        "year": 2017,
        "citationCount": 173000,
        "url": "https://en.wikipedia.org/wiki/Attention_Is_All_You_Need"
    },
    {
        "title": "Highly Accurate Protein Structure Prediction with AlphaFold",
        "year": 2021,
        "citationCount": 8965,
        "url": "https://www.zeta-alpha.com/post/must-read-the-100-most-cited-ai-papers-in-2022"
    },
    {
        "title": "Language Models are Few-Shot Learners",
        "year": 2020,
        "citationCount": 8070,
        "url": "https://www.zeta-alpha.com/post/must-read-the-100-most-cited-ai-papers-in-2022"
    },
    {
        "title": "An Image is Worth 16x16 Words: Transformers for Image Recognition at Scale",
        "year": 2020,
        "citationCount": 11914,
        "url": "https://www.zeta-alpha.com/post/must-read-the-100-most-cited-ai-papers-in-2022"
    },
    {
        "title": "LLaMA: Open and Efficient Foundation Language Models",
        "year": 2023,
        "citationCount": 8534,
        "url": "https://www.zeta-alpha.com/post/analyzing-the-homerun-year-for-llms-the-top-100-most-cited-ai-papers-in-2023-with-all-medals-for-o"
    },
    {
        "title": "Segment Anything",
        "year": 2023,
        "citationCount": 5293,
        "url": "https://www.zeta-alpha.com/post/analyzing-the-homerun-year-for-llms-the-top-100-most-cited-ai-papers-in-2023-with-all-medals-for-o"
    },
    {
        "title": "GPT-4 Technical Report",
        "year": 2023,
        "citationCount": 3384,
        "url": "https://www.zeta-alpha.com/post/analyzing-the-homerun-year-for-llms-the-top-100-most-cited-ai-papers-in-2023-with-all-medals-for-o"
    },
    {
        "title": "BLIP-2: Bootstrapping Language-Image Pre-training with Frozen Image Encoders and Large Language Models",
        "year": 2023,
        "citationCount": 3099,
        "url": "https://www.zeta-alpha.com/post/analyzing-the-homerun-year-for-llms-the-top-100-most-cited-ai-papers-in-2023-with-all-medals-for-o"
    },
    {
        "title": "YOLOv4: Optimal Speed and Accuracy of Object Detection",
        "year": 2020,
        "citationCount": 8014,
        "url": "https://www.zeta-alpha.com/post/must-read-the-100-most-cited-ai-papers-in-2022"
    },
    {
        "title": "Exploring the Limits of Transfer Learning with a Unified Text-to-Text Transformer",
        "year": 2020,
        "citationCount": 5906,
        "url": "https://www.zeta-alpha.com/post/must-read-the-100-most-cited-ai-papers-in-2022"
    }
];

    # Filtrering (gælder kun for dummy data)
    filtered = []
    for paper in dummy_data:
        if year_condition == "after" and paper["year"] <= year:
            continue
        elif year_condition == "before" and paper["year"] >= year:
            continue
        elif year_condition == "equal to" and paper["year"] != year:
            continue

        if paper["citationCount"] < min_citations:
            continue

        filtered.append(paper)
        if len(filtered) >= limit:
            break

    return filtered

    """
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
    
    """
