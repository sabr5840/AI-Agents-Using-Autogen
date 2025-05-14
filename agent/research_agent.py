import os
import sys
import re
import json


# Tilføj projektets rodmappe til sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from autogen import AssistantAgent, UserProxyAgent, register_function
from config import LLM_CONFIG
from tools.semantic_scholar_search import search_papers
from agent.agent_evaluation import evaluate_response


def get_user_input():
    topic = input("Enter the subject (e.g. 'Artificial Intelligence'): ")
    year_condition = input("Enter the years: 'before', 'after' or 'equal to' [year]: ").strip().lower()

    while year_condition not in ["before", "after", "equal to"]:
        print("Invalid input. Please choose 'before', 'after' or 'equal to'.")
        year_condition = input("Enter the years: 'before', 'after' or 'equal to' [year]: ").strip().lower()

    year = input(f"Enter the year for {year_condition}: ")
    while not year.isdigit() or int(year) < 1990:
        print("Invalid year. Please enter a valid number from 1990 and up.")
        year = input(f"Enter the year for {year_condition}: ")

    citations = input("Enter minimum number of citations: ")
    while not citations.isdigit():
        print("Invalid number of citations. Please enter a valid number.")
        citations = input("Enter minimum number of citations: ")

    return topic, year_condition, int(year), int(citations)


def format_papers(raw_response: str) -> str:
    paper_pattern = re.compile(
        r"\*\*Title:\*\* (.*?)\n\s+- \*\*Year:\*\* (\d{4})\n\s+- \*\*Citation Count:\*\* (\d+)\n\s+- \*\*URL:\*\* \[(.*?)\]\((.*?)\)",
        re.DOTALL
    )

    matches = paper_pattern.findall(raw_response)
    formatted = []

    for i, (title, year, citations, _, url) in enumerate(matches, 1):
        formatted.append(
            f"{i}. {title}\n📅 Year:  {year}\n📈 Citation Count: {citations}\n🔗 URL: {url}\n"
        )

    return "\n".join(formatted) if formatted else raw_response


def format_evaluation(evaluation: dict) -> str:
    if "error" in evaluation:
        return f"Fejl i evaluering: {evaluation['error']}"

    return (
        f"* Relevans: {evaluation['relevance']}\n"
        f"* Kvalitet: {evaluation['quality']}\n"
        f"* Detaljerigdom: {evaluation['detail']}\n"
        f"* Robusthed: {evaluation['robustness']}\n"
        f"* Nøjagtighed: {evaluation['accuracy']}\n\n"
        f"Feedback:\n{evaluation['feedback']}"
    )


def main():
    topic, year_condition, year, citations = get_user_input()

    message_body = (
        f"Find research papers on '{topic}' published {year_condition} {year} "
        f"with at least {citations} citations. When you've found suitable results, just return them and end the conversation."
    )

    user_proxy = UserProxyAgent(
        name="User",
        human_input_mode="NEVER",
        code_execution_config=False
    )

    assistant = AssistantAgent(
        name="ResearchAssistant",
        llm_config=LLM_CONFIG
    )

    register_function(
        search_papers,
        caller=assistant,
        executor=user_proxy,
        name="search_papers",
        description="Search Semantic Scholar for papers matching a topic, year condition, and minimum citations"
    )

    chat_result = user_proxy.initiate_chat(
        assistant,
        message=message_body,
        summary_method="last_msg",
        max_turns=3
    )

    agent_response = chat_result.summary
    evaluation = evaluate_response(message_body, agent_response)

    print("\n📚 Agentens svar:\n")
    print(format_papers(agent_response))
    print("\n🔍 Evaluering\n")
    print(format_evaluation(evaluation))


if __name__ == "__main__":
    main()
