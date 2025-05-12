import os
from dotenv import load_dotenv


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
