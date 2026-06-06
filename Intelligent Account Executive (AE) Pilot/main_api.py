from fastapi import FastAPI
from pydantic import BaseModel as PyBaseModel, Field
from typing import List, Optional

# LangChain / LangGraph Imports
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.tools import DuckDuckGoSearchRun
from langgraph.prebuilt import create_react_agent

# Initialize FastAPI App
app = FastAPI()

# Initialize our local tool-capable model
# Ensure you have run 'ollama pull llama3.1'
llm = ChatOllama(model="llama3.1", temperature=0)

# --- PHASE 1 SETUP: Structured Extraction ---
class CallInsights(PyBaseModel):
    company_name: str = Field(description="The name of the prospect's company.")
    competitors_mentioned: List[str] = Field(description="Any competitor tools mentioned.")

extraction_prompt = ChatPromptTemplate.from_messages([
    ("system", "Analyze the transcript and extract the company and competitors into the requested schema."),
    ("human", "{transcript_summary}")
])

# Bind structured output
structured_llm = llm.with_structured_output(CallInsights, method="json_schema")
extraction_chain = extraction_prompt | structured_llm

# --- PHASE 2 SETUP: Autonomous Agent ---
search_tool = DuckDuckGoSearchRun()
agent_executor = create_react_agent(llm, [search_tool])


# --- API INPUT SCHEMA ---
# This defines what data n8n needs to send to our Python API
class TranscriptInput(PyBaseModel):
    summary: str

# --- THE WEBHOOK ENDPOINT ---
@app.post("/process-transcript")
async def process_transcript(data: TranscriptInput):
    print(f"\n[1/3] Received transcript from n8n. Starting extraction...")
    
    # 1. Run Phase 1: Extract variables programmatically
    insights: CallInsights = extraction_chain.invoke({"transcript_summary": data.summary})
    print(f"-> Extracted Company: {insights.company_name}")
    print(f"-> Extracted Competitors: {insights.competitors_mentioned}")
    
    # 2. Check if competitors were found before firing the agent
    research_report = "No competitors mentioned to research."
    
    if insights.competitors_mentioned:
        print(f"\n[2/3] Competitors found. Launching LangGraph search agent...")
        
        query = (
            f"Find 2-3 recent distinct competitive advantages or pricing facts for "
            f"{', '.join(insights.competitors_mentioned)} that a rival salesperson could use."
        )
        
        # Run Phase 2: Autonomous Agent loop
        agent_response = agent_executor.invoke({"messages": [("user", query)]})
        research_report = agent_response["messages"][-1].content
    else:
        print(f"\n[2/3] Skipping research agent (no competitors mentioned).")

    print(f"\n[3/3] Workflow complete. Returning payload back to n8n.")
    
    # 3. Return the combined data straight back to n8n as a clean JSON response
    return {
        "status": "success",
        "company": insights.company_name,
        "competitors_evaluated": insights.competitors_mentioned,
        "raw_research": research_report
    }
