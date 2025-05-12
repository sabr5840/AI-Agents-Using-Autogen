# AI Agent for Research Paper Search

Dette projekt implementerer en AI-agent ved hjælp af Autogen, som kan finde forskningsartikler baseret på brugerinput.

## 🔍 Formål

Formålet med projektet er at udvikle en agent, som automatisk kan:
- Søge efter forskningsartikler om et givet emne
- Filtrere efter publiceringsår (før, efter eller lig med et bestemt år)
- Filtrere efter minimum antal citationer

## ⚙️ Hvordan virker det?

Agenten benytter følgende komponenter:

- **Autogen**-framework til at opbygge kommunikationen mellem bruger og AI-assistent
- En funktion (`search_papers`) som søger i Semantic Scholar API og returnerer relevante artikler
- Et simpelt input-flow hvor brugeren bliver bedt om at indtaste emne, årstal og citationskrav
- Agenten bruger værktøjet til at finde artikler og returnerer dem direkte til brugeren

## 🧠 Eksempel på brug

1. Brugeren bliver spurgt om:
   - Emne (f.eks. "Artificial Intelligence")
   - Om artiklerne skal være før, efter eller lig med et givent årstal
   - Hvilket årstal
   - Minimum antal citationer

2. Agenten formulerer en forespørgsel og kalder funktionen `search_papers`.

3. Resultatet er en liste med forskningsartikler, som opfylder kravene.

## 🗂 Projektstruktur

- `agent/research_agent.py`: Selve agentens logik og brugerinput
- `tools/semantic_scholar_search.py`: Værktøjsfunktion til at søge i Semantic Scholar API
- `config.py`: Indeholder konfiguration til den cloud-baserede LLM
- `.env`: Indeholder Mistral API-nøgle (med i `.gitignore`)

