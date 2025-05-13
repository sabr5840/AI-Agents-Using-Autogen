# agent/agent_evaluation.py

# STEP 1: Evaluation Criteria
"""
| Kriterium        | Beskrivelse |
|------------------|-------------|
| Relevans         | Passer artiklerne til brugerens emne og krav (årstal, tema, type)? |
| Kvalitet         | Er artiklerne fra troværdige kilder og akademisk valide (fx citations, journal)? |
| Detaljegrad      | Indeholder output nok info (titel, forfatter, årstal, link, citations, etc.)? |
| Robusthed        | Kan agenten stadig levere noget meningsfuldt ved tvetydige eller ufuldstændige prompts? |
| Nøjagtighed      | Matcher de præsenterede artikler faktisk de nævnte data (fx citations ≥100)? |
"""

# STEP 2: Sample Test Prompts
"""
Typiske:
- "Find 3 artikler om AI i sundhedssektoren siden 2020 med over 100 citationer"
- "Vis forskning om bæredygtig energi i Europa, gerne nyere end 2018"

Tvetydige:
- "Jeg vil gerne have noget om klima"
- "Find mig banebrydende forskning – det skal bare være godt"

Komplekse:
- "Find artikler om deep learning til kræftdiagnose, der også inkluderer open-source kode"
"""

# STEP 3: LLM-as-Critic Evaluation
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from autogen import ConversableAgent
from agent.research_agent import generate_reply  # Denne import skal bruges korrekt
from config import LLM_CONFIG

# Opret kritik-agent med Mistral
critic = ConversableAgent(
    name="Critic",
    llm_config=LLM_CONFIG
)

def evaluate_response(user_prompt: str, agent_response: str) -> str:
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

Provide your evaluation as JSON with these fields:
- relevance
- quality
- detail
- robustness
- accuracy
- feedback (a concise explanation of the evaluation using examples from the agent’s response)
"""

    try:
        # Generating the evaluation using the critic
        evaluation_response = critic.generate_reply(messages=[critic_prompt])
        # Assuming the response is in the form of a JSON-like structure, return it directly
        return evaluation_response
    except Exception as e:
        # Return a more detailed error message
        return f"Error during evaluation: {str(e)}"

# Eksempel: Samlet flow med generate_reply og evaluering
if __name__ == "__main__":
    prompt = "Find artikler om AI i sundhedssektoren siden 2020 med over 100 citationer"
    print(f"\nPrompt: {prompt}")
    
    # Kald generate_reply() med brugerens prompt og få agentens svar
    agent_output = generate_reply(user_prompt=prompt)  # Passer input korrekt
    print(f"\nAgentens svar:\n{agent_output}")
    
    # Evaluering af agentens output
    evaluation = evaluate_response(prompt, agent_output)
    print(f"\nEvaluering:\n{evaluation}")
