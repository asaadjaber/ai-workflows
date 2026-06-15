import requests
import re

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "llama3"

def call_ollama(system_prompt: str, user_prompt: str) -> str:
    """Core local LLM executor tool."""
    combined_prompt = f"System: {system_prompt}\nUser: {user_prompt}\nResponse:"
    payload = {"model": MODEL_NAME, "prompt": combined_prompt, "stream": False}
    try:
        response = requests.post(OLLAMA_URL, json=payload)
        response.raise_for_status()
        return response.json().get("response", "").strip()
    except Exception as e:
        print(f"Ollama network error: {e}")
        return ""

def native_faithfulness_eval(retrieved_context: str, generated_output: str) -> float:
    """
    An isolated, native implementation of a statement-verification audit loop.
    Completely eliminates the need for the broken Ragas package.
    """
    print("📋 Step A: Extracting explicit factual statements from generation...")
    
    extract_prompt = f"""
    Analyze the following text payload. Break it down into a list of distinct, singular factual statements or claims made about the product/movie.
    Format your response as a clean, simple bulleted list starting with '-' for each item.
    Do not add an introduction or conclusion.
    
    [TEXT PAYLOAD]: {generated_output}
    """
    raw_statements = call_ollama("You output clean bulleted lists only.", extract_prompt)
    
    # Parse the bullet points out into a native Python list
    statements = [line.strip("- ").strip() for line in raw_statements.split("\n") if line.strip()]
    if not statements:
        return 0.0
    
    total_statements = len(statements)
    verified_statements = 0
    
    print(f"🔎 Step B: Auditing {total_statements} statement(s) against Weaviate Context ledger...")
    
    # Audit each claim individually
    for statement in statements:
        verify_prompt = f"""
        You are a rigid legal fact-checker. Determine if the [CLAIM] can be directly inferred from the [GROUND TRUTH CONTEXT].
        If the context directly supports the claim, output exactly: VERIFIED
        If the context does not mention the claim, contradicts it, or if the claim invents details, output exactly: HALLUCINATION
        Do not explain your reasoning. Output exactly one of those two words.
        
        [GROUND TRUTH CONTEXT]: {retrieved_context}
        [CLAIM]: {statement}
        """
        verdict = call_ollama("You output singular classification keywords only.", verify_prompt).upper()
        
        if "VERIFIED" in verdict:
            verified_statements += 1
            print(f"  ✅ [VALID]: {statement}")
        else:
            print(f"  ❌ [HALLUCINATION DETECTED]: {statement}")
            
    # Calculate faithfulness ratio
    score = verified_statements / total_statements
    return round(score, 2)
