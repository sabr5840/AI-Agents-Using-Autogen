import os
from dotenv import load_dotenv
from autogen import AssistantAgent, UserProxyAgent


load_dotenv()

LLM_CONFIG = {
    "config_list": [
        {
            "model": "open-mistral-nemo",
            "api_key": os.getenv("MISTRAL_API_KEY"),
            "api_type": "mistral",
            "temperature": 0.0,
            "stream": False,
        }
    ]
}


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

# Start samtale
user_proxy.initiate_chat(
    assistant,
    message="Find en forskningsartikel om kunstig intelligens udgivet efter 2020 med mindst 50 citationer."
)




