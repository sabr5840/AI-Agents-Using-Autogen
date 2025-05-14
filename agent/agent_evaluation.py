# agent/agent_evaluation.py

# STEP 1: Evaluation Criteria
"""
| Kriterium        | Beskrivelse |
|------------------|-------------|
| Relevans         | Passer artiklerne til brugerens emne og krav (årstal, emne mm,)? |
| Kvalitet         | Er artiklerne fra troværdige kilder og akademisk valide ?        |
| Detaljegrad      | Indeholder output nok info (titel, årstal, link, citations, etc.)? |
| Robusthed        | Kan agenten stadig levere noget meningsfuldt ved tvetydige eller ufuldstændige prompts? |
| Nøjagtighed      | Matcher de præsenterede artikler faktisk de nævnte data  |
"""

# STEP 2: Sample Test Prompts

"""

Typical Prompts (typiske brugsscenarier):

{"topic": "AI", "year_condition": "after", "year": 2015, "min_citations": 100, "limit": 5}

{"topic": "climate change", "year_condition": "before", "year": 2010, "min_citations": 50, "limit": 5}


Complex Requests (flere krav kombineret):

{"topic": "AI in healthcare", "year_condition": "after", "year": 2018, "min_citations": 150, "limit": 5}

{"topic": "renewable energy", "year_condition": "before", "year": 2020, "min_citations": 200, "limit": 5}


Ambiguous Prompts (uklare eller tvetydige forespørgsler):

{"topic": "deep learning", "year_condition": "after", "year": 2010, "min_citations": 100, "limit": 5}

{"topic": "health", "year_condition": "before", "year": 2000, "min_citations": 50, "limit": 5}


Edge Cases or Errors (grænsetilfælde og fejlscenarier):

{"topic": "quantum computing", "year_condition": "after", "year": 1800, "min_citations": 50, "limit": 5}

{"topic": "Xc$#2399", "year_condition": "after", "year": 2015, "min_citations": 0, "limit": 5}


"""

# STEP 3: LLM-as-Critic Evaluation
import os
import re
import sys
import json
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from autogen import ConversableAgent
from config import LLM_CONFIG

# Evalueringsagent
critic = ConversableAgent(
    name="Critic",
    llm_config=LLM_CONFIG
)

def evaluate_response(user_prompt: str, agent_response: str) -> dict:
    critic_prompt = f"""
    You are evaluating an academic research assistant AI agent.

    Evaluate the agent's output based on the following criteria:
    - Relevance (1-5): Are the results aligned with the user's research topic and filters?
    - Quality (1-5): Are the articles from credible sources with good academic standing?
    - Detail (1-5): Are details like title, author, year, citations, and URL clearly presented?
    - Robustness (1-5): Did the agent handle vague or incomplete prompts meaningfully?
    - Accuracy (1-5): Do the listed papers match the user's filters (e.g., year, citations)?

    User Prompt: {user_prompt}
    Agent Response: {agent_response}

    Respond ONLY with a valid JSON object in the following format:
    {{
        "relevance": int (1-5),
        "quality": int (1-5),
        "detail": int (1-5),
        "robustness": int (1-5),
        "accuracy": int (1-5),
        "feedback": string
    }}
    """

    try:
        evaluation_response = critic.generate_reply(messages=[{"role": "user", "content": critic_prompt}])
        content = evaluation_response.get("content", "{}")

        json_str = re.search(r"\{.*\}", content, re.DOTALL).group()
        return json.loads(json_str)

    except json.JSONDecodeError:
        return {"error": "Invalid JSON from critic"}
    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}

