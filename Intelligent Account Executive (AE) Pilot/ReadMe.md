# Intelligent Account Executive (AE) Copilot

This mini-project extends a traditional n8n sales workflow by routing unstructured call data to a local LangChain and LangGraph pipeline. Using a local model via Ollama, the system extracts key competitor variables and deploys an autonomous ReAct agent to scrape the web via DuckDuckGo. The synthesized competitive intelligence is then structurally synced back to Airtable via n8n endpoints.

## The 3 Core Phases Built inside LangChain:
* **Phase 1: Smart Ingestion (Chains & Structured Output):** Ingests raw sales transcripts or summaries and uses `ChatOllama` coupled with **Pydantic** validation to enforce a strict JSON schema (`CallInsights`) that extracts the target company name and competitors mentioned.
* **Phase 2: Deep-Dive Researcher (Autonomous Agents & Tools):** Uses a modern **LangGraph ReAct agent** loop. If competitors are detected in Phase 1, the local model autonomously fires up a `DuckDuckGoSearchRun` tool, crawls the web for recent competitive advantages, synthesizes the data, and builds a strategic sales brief.
* **Phase 3: Contextual Pitcher (Stateful Memory Chain):** A local terminal chat layout utilizing `MessagesPlaceholder` that retains historical context natively so an Account Executive can iteratively chat with the AI to refine hyper-targeted outreach templates based on the agent's research.

## Tech Stack

* **Language:** Python 3.14+
* **Frameworks:** LangChain (Core/Ollama), LangGraph, FastAPI, Uvicorn
* **Local LLM Engine:** Ollama (Running `llama3.1`)
* **Tunneling & Tooling:** ngrok, DuckDuckGo Search API
* **Orchestration:** n8n (Cloud or Self-Hosted), Airtable

## Setup

Set up a Python virtual environment 

`python3 -m venv .venv`

`source .venv/bin/activate`

Fire up the FastAPI server  

`uvicorn main_api:app --reload --port 8000`

Expose local port via grok

`Grok http 8000`

## Results

- **Model Interchangeability:** Transitioning from cloud OpenAI engines to a local model requires updating only a single constructor line, proving the structural stability of LangChain's ecosystem abstractions.
- **Agent vs. Chain Logic:** Learned how an Agent uses an external evaluation graph (LangGraph) to parse data, call scripts, and conditionally choose whether to pivot or finalize execution loops dynamically.

