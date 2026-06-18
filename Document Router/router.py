import os
import requests

LOCAL_OLLAMA_ENDPOINT="http://localhost:11434/api/generate"

def call_llm(system_prompt, user_text) -> str:

    combined_prompt = f"System: {system_prompt}\nUser: Analyze this text: {user_text}"

    payload = {
        "model": "llama3",
        "prompt": combined_prompt,
        "stream": False
    }

    response = requests.post(LOCAL_OLLAMA_ENDPOINT, json=payload)
    response.raise_for_status()
    text_response = response.json().get("response")
    return text_response

def classify_and_summarize(document_content) -> (str, str):

    system_prompt = f"""
        You are a highly isolated routing engine. Analyze the text and return exactly two lines of output with a specific 
        delimiter like a colon: 

        Example expected output format: 

        CATEGORY: LEGAL
        SUMMARY: This document outlines a standard non-disclosure agreement regarding intellectual property.
    """

    raw_string = call_llm(system_prompt=system_prompt, user_text=document_content)

    print("raw_string", raw_string)

    lines = raw_string.split("\n")

    extracted_category = "UNKNOWN"
    extracted_summary = "No summary generated."

    for line in lines: 

        cleaned_line = line.strip()

        if "CATEGORY:" in cleaned_line:
            start_index_category = cleaned_line.find("CATEGORY:")
            extracted_category = cleaned_line[start_index_category + 9:].strip()

        elif "SUMMARY:" in cleaned_line:
            start_index_summary = cleaned_line.find("SUMMARY:")
            extracted_summary = cleaned_line[start_index_summary + 8:].strip()

    return (extracted_category, extracted_summary)

if __name__ == "__main__":

    for doc in os.listdir("documents"):

        file_path = f"documents/{doc}"

        with open(file_path, 'r', encoding='latin1') as file: 
            content = file.read()

            category, summary = classify_and_summarize(document_content=content)

            directory = f"storage/{category}"

            os.makedirs(directory, exist_ok=True)

            # create file inside new directory and write to it

            file_name = f"summary_of_{doc}.txt"

            file_path = os.path.join(directory, file_name)

            with open(file_path, 'w') as f:
                f.write(summary)
