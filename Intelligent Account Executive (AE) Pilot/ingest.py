import os
from typing import List, Optional
from pydantic import BaseModel, Field
#from langchain_openai import ChatOpenAI
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate

# 1. Define the exact structure you want to extract using Pydantic
class CallInsights(BaseModel):
    company_name: str = Field(description="The name of the prospect's company.")
    pain_points: List[str] = Field(description="List of core problems or challenges the prospect mentioned.")
    budget_hint: Optional[str] = Field(description="Any mention of budget, pricing constraints, or tier preferences.")
    competitors_mentioned: List[str] = Field(description="Any competitor tools or current solutions they are using.")
    next_steps: List[str] = Field(description="Action items agreed upon during the call.")

# 2. Initialize the LLM
# LangChain automatically looks for the OPENAI_API_KEY environment variable
# llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
llm = ChatOllama(model="llama3", temperature=0)

# 3. Tell the LLM to strictly conform to our Pydantic schema
structured_llm = llm.with_structured_output(CallInsights)

# 4. Create a dynamic prompt template
prompt_template = ChatPromptTemplate.from_messages([
    (
        "system",
        "You are an expert sales analyst. Analyze the following call summary or transcript "
        "and extract key operational insights precisely."
    ),
    ("human", "{transcript_summary}")
])

# 5. Chain them together using LCEL (LangChain Expression Language)
# The pipeline passes the input dictionary through the prompt, then to the structured LLM
extraction_chain = prompt_template | structured_llm

# --- Test Run ---
if __name__ == "__main__":
    # Mock data representing what you would pull from Airtable
    sample_summary = """
    FinPay (85 agents across three regions) is experiencing rapid growth and a fragmented 
    support stack (Zendesk, Intercom, separate KB, internal tools). Key goals are to reduce 
    first-response time (from ~6 hours to <1 hour), improve resolution rates, and automate 
    25–30% of inbound Tier 1 inquiries without degrading customer experience. 
    Michael (VP Customer Support) is interested in AI for repetitive tasks but is 
    cautious about accuracy, compliance, integration complexity, change management, and 
    ROI. Budget range is $75k–$150k annually. Next step agreed: a 45-minute workflow 
    session with a solutions consultant including FinPay’s Director of Support Operations 
    and Zendesk admin.
    """
    
    print("Analyzing transcript...")
    
    # Invoke the chain
    result: CallInsights = extraction_chain.invoke({"transcript_summary": sample_summary})
    
    # Look at the clean, typed output
    print("\n--- Extracted Data Structure ---")
    print(f"Company: {result.company_name}")
    print(f"Pain Points: {result.pain_points}")
    print(f"Competitors: {result.competitors_mentioned}")
    print(f"Budget Info: {result.budget_hint}")
    print(f"Next Steps: {result.next_steps}")
