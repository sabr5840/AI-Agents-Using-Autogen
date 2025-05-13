import os
import sys

# Gør det muligt at importere moduler fra parent-mappen
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from autogen import AssistantAgent, UserProxyAgent, register_function
from config import LLM_CONFIG
from tools.semantic_scholar_search import search_papers

# Opret AI-agent og bruger
user_proxy = UserProxyAgent(
    name="User",
    human_input_mode="ALWAYS",  # Brugeren skriver manuelt
    code_execution_config=False
)

assistant = AssistantAgent(
    name="ResearchAssistant",
    llm_config=LLM_CONFIG
)

# Registrerer funktionen 'search_papers', så assistenten kan bruge den
register_function(
    search_papers,
    caller=assistant,
    executor=user_proxy,
    name="search_papers",
    description="Search Semantic Scholar for papers matching a topic, year condition, and minimum citations"
)

# Funktion til at få brugerens input
def get_user_input():
    topic = input("Enter the subject (e.g. 'Artificial Intelligence'): ")
    year_condition = input("Enter the years: 'before', 'after' or 'equal to' [year]: ")
    year = input(f"Enter the year for {year_condition}: ")
    while not year.isdigit() or int(year) < 1990:
        print("Invalid year. Please enter a valid number.")
        year = input(f"Enter the year for {year_condition}: ")
    citations = input("Enter minimum number of citations: ")
    while not citations.isdigit():
        print("Invalid number of citations. Please enter a valid number.")
        citations = input("Enter minimum number of citations: ")
    return topic, year_condition, int(year), int(citations)

# Hent input fra bruger
topic, year_condition, year, citations = get_user_input()

# Skab en forespørgselsbesked
message_body = (
    f"Find research papers on '{topic}' published {year_condition} {year} "
    f"with at least {citations} citations. Use the tool `search_papers` if needed."
)

# Start samtalen (Autogen håndterer tools, så du behøver ikke gøre det manuelt her)
user_proxy.initiate_chat(
    assistant,
    message=message_body
)
