import os
import sys
import requests

# 1. State Management Setup
# This dictionary acts as the single source of truth passed between agent functions.
debate_state = {
    "topic": "Is Software-as-a-Service (SaaS) dead for independent developers?",
    "pro_argument": "",
    "con_argument": "",
    "final_judgment": ""
}

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "llama3"  # Ensure you have pulled this locally via: ollama pull llama3

def call_local_llm(prompt: str) -> str:
    """Helper utility to route raw strings to your local Ollama instance."""
    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": False
    }
    try:
        response = requests.post(OLLAMA_URL, json=payload)
        response.raise_for_status()
        return response.json().get("response", "").strip()
    except requests.exceptions.RequestException as e:
        print(f"\n❌ Error connecting to Ollama: {e}")
        sys.exit(1)

# 2. Agent Node Definitions
def run_optimistic_agent(state: dict) -> dict:
    """Agent 1: Defends the topic aggressively using optimistic economic logic."""
    print("🤖 [Optimist Agent] Formulating supporting case study arguments...")
    
    prompt = f"""
    You are an expert tech optimist, venture capitalist, and startup founder.
    Your task is to provide a concise, sharp argument defending this stance:
    Stance: "{state['topic']}" - Argue YES, explaining why this is true.
    
    Focus on structural economic shifts, modern tooling efficiencies, and market changes.
    Be punchy, limit your response to two strong paragraphs, and do not introduce yourself.
    """
    
    # Mutate the shared clipboard state natively
    state["pro_argument"] = call_local_llm(prompt)
    return state

def run_skeptic_agent(state: dict) -> dict:
    """Agent 2: Attacks the topic and counter-analyzes the opposing perspective."""
    print("🤖 [Skeptic Agent] Analyzing opposition and formulating counter-claims...")
    
    prompt = f"""
    You are a realistic tech pessimist, senior software engineer, and economic analyst.
    Your task is to counter-argue this stance: "{state['topic']}".
    
    You have been handed the following arguments from an optimist:
    ---
    {state['pro_argument']}
    ---
    
    Write a concise counter-argument. Directly tear down the optimist's points or offer a 
    sobering alternative reality. Limit to two strong paragraphs, and do not introduce yourself.
    """
    
    state["con_argument"] = call_local_llm(prompt)
    return state

def run_judge_agent(state: dict) -> dict:
    """Agent 3: Synthesizes both arguments and outputs a comprehensive executive summary."""
    print("⚖️ [Judge Agent] Weighing evidence and compiling final report...")
    
    prompt = f"""
    You are a neutral, objective Research Director for a major technology firm.
    Review the following debate transcript concerning this core topic: "{state['topic']}"
    
    [PRO SIDE ARGUMENT]:
    {state['pro_argument']}
    
    [CON SIDE ARGUMENT]:
    {state['con_argument']}
    
    Your task is to write a highly objective final executive summary. 
    1. Summarize the merit of each side's best point.
    2. Deliver a final data-driven verdict or synthesis.
    
    Format your response entirely in beautiful Markdown with clear headers.
    """
    
    state["final_judgment"] = call_local_llm(prompt)
    return state

# 3. Execution Pipeline Orchestration
if __name__ == "__main__":
    print(f"🚀 Starting Multi-Agent Debate Session")
    print(f"📌 Target Topic: '{debate_state['topic']}'\n")
    print("="*60)
    
    # Run Node 1: Optimist frames the debate
    debate_state = run_optimistic_agent(debate_state)
    print(f"\n📢 OPTIMIST ARGUMENT:\n{debate_state['pro_argument']}\n")
    print("="*60)
    
    # Run Node 2: Skeptic responds to the exact state content
    debate_state = run_skeptic_agent(debate_state)
    print(f"\n📢 SKEPTIC COUNTER-ARGUMENT:\n{debate_state['con_argument']}\n")
    print("="*60)
    
    # Run Node 3: Judge creates a report compiling the outputs
    debate_state = run_judge_agent(debate_state)
    
    print("\n👑 --- FINAL JUDGE EXECUTIVE REPORT ---")
    print(debate_state["final_judgment"])
    
    # Optional Challenge: Save the output state cleanly to disk
    with open("debate_verdict.md", "w") as f:
        f.write(debate_state["final_judgment"])
    print("\n💾 Saved final verdict to debate_verdict.md successfully!")
