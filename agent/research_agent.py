import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from autogen import AssistantAgent, UserProxyAgent, register_function
from config import LLM_CONFIG
from tools.semantic_scholar_search import search_papers

# Opret AI-agent og bruger
user_proxy = UserProxyAgent(
    name="User",
    human_input_mode="ALWAYS",  # Opdateret værdi
    code_execution_config=False
)

assistant = AssistantAgent(
    name="ResearchAssistant",
    llm_config=LLM_CONFIG
)

# Registrerer funktionen 'search_papers', som kan bruges af assistenten og eksekveres af bruger-proxyen
register_function(
    search_papers,
    caller=assistant,
    executor=user_proxy,
    name="search_papers",
    description="Search Semantic Scholar for papers matching a topic, year condition, and minimum citations"
)

# Funktion til at få brugerens input til emne, år og citater
def get_user_input():
    topic = input("Enter the subject (e.g. 'Artificial Intelligence'): ")
    year_condition = input("Enter the years: 'before', 'after' or 'equal to' [year]: ")
    year = input(f"Enter the year for {year_condition}: ")
    while not year.isdigit():
        print("Invalid year. Please enter a valid number.")
        year = input(f"Enter the year for {year_condition}: ")
    citations = input("Enter minimum number of citations: ")
    while not citations.isdigit():
        print("Invalid number of citations. Please enter a valid number.")
        citations = input("Enter minimum number of citations: ")
    return topic, year_condition, int(year), int(citations)

# Henter brugerens input
topic, year_condition, year, citations = get_user_input()

# Opretter en besked, der beskriver forespørgslen til assistenten
message_body = (
    f"Find research papers on '{topic}' published {year_condition} {year}"
    f" with at least {citations} citations."
)

# Starter samtale med assistenten
user_proxy.initiate_chat(
    assistant,
    message=message_body
)




