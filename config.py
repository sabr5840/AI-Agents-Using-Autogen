import os
from dotenv import load_dotenv

load_dotenv()

LLM_CONFIG = {
    "config_list": [
        {
            "model": "mistral-large-latest",  #open-mistral-nemo
            "api_key": os.getenv("MISTRAL_API_KEY"),
            "api_type": "mistral",
            "api_rate_limit": 0.25,
            "repeat_penalty": 1.1,
            "temperature": 0.0,
            "seed": 42,
            "stream": False,
            "cache_seed": None,
            "native_tool_calls": True,
            "tool_choice": "auto",
        }
    ]
}

