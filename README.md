Installer nødvendige pakker
Kør følgende én gang i terminalen, når du er i det virtuelle miljø:

pip install git+https://github.com/patrickstolc/autogen.git@0.2#egg=autogen-agentchat
pip install autogen==0.3.1 mistralai==1.2.3 ollama==0.3.3 fix-busted-json==0.0.18

Forklaring
autogen-agentchat: En særlig version af Autogen, tilpasset til cloud-LLMs og rate limits.
autogen==0.3.1: Hovedframeworket.
mistralai: API-klienten til Mistral AI.
ollama, fix-busted-json: Understøttende biblioteker.

Installér python-dotenv
Husk at installere python-dotenv, så du kan bruge .env filer:

pip install python-dotenv

Python Version
For at hente de nødvendige pakker skal du sikre dig, at du bruger Python version 3.11.10.
