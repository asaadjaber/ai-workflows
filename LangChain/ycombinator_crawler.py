import re
import time
import requests
from bs4 import BeautifulSoup
from langchain_core.tools import tool
from langchain.chat_models import init_chat_model
from langchain_core.messages import ToolMessage

def fetch_yc_batch_links(batch_name: str) -> list:
    """
    Fetches the static, open-source community batch dataset for YC companies,
    with a safeguard to prevent corrupted year slug strings.
    """
    # Force a clean lowercase string (e.g., "spring 2026" or "spring 202026")
    clean_name = batch_name.strip().lower().replace(" ", "-")
    
    # ✨ FIX: If the model accidentally double-injects the year (e.g., 202026), fix it to 2026
    clean_name = re.sub(r"202026", "2026", clean_name)
    
    url = f"https://yc-oss.github.io/api/batches/{clean_name}.json"
    
    print(f"📡 Pulling public batch archive dataset: {url}...")
    
    try:
        response = requests.get(url, timeout=10, verify=False)
        response.raise_for_status()
        companies_data = response.json()
        
        urls = []
        for company in companies_data:
            slug = company.get("slug")
            if slug:
                urls.append(f"https://www.ycombinator.com/companies/{slug}")
                
        print(f"✨ Successfully discovered {len(urls)} company profiles for {batch_name}.")
        return urls
    except Exception as e:
        print(f"❌ Failed to fetch batch archive: {e}")
        return []

@tool 
def batch_word_occurrences(batch: str, target_word: str) -> str:
    """
    Scrapes the profile page of every individual startup within a designated 
    Y Combinator batch, calculates the combined occurrences of a target keyword, 
    and tracking total sites crawled.
    
    Args:
        batch: The clean batch identification name string (e.g., "Spring 2026", "Winter 2026").
        target_word: The explicit string token to look for across the profiles.
    """
    print(f"\n⚡ [Tool Triggered] Launching crawl for batch '{batch}' tracking keyword '{target_word}'...")
    
    # 1. Fetch all profile URLs for the requested batch
    profile_urls = fetch_yc_batch_links(batch)
    
    if not profile_urls:
        return "Failed to retrieve any startup profiles for this batch."
        
    total_occurrences = 0
    sites_visited_count = 0
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
    }
    
    # 2. Iterate and scrape each individual company profile
    for idx, url in enumerate(profile_urls, start=1):
        try:
            # Bypass local SSL bundle issues using verify=False
            response = requests.get(url, headers=headers, timeout=5, verify=False)
            sites_visited_count += 1
            
            if response.status_code != 200:
                continue
                
            soup = BeautifulSoup(response.text, "html.parser")
            
            # Wipe away code blocks and interface layout elements
            for junk in soup(["script", "style", "nav", "footer", "header"]):
                junk.extract()
                
            clean_text = soup.get_text()
            
            # Search for variations or extensions matching your root choice (e.g., agent, agents, agentic)
            pattern = rf"\b{re.escape(target_word)}\w*"
            matches = re.findall(pattern, clean_text, flags=re.IGNORECASE)
            
            total_occurrences += len(matches)
            
            # Print a clean diagnostic heartbeat every 5 sites so you know the script is humming along
            if idx % 5 == 0 or idx == len(profile_urls):
                print(f"   ↳ Progress: Visited {sites_visited_count}/{len(profile_urls)} sites... Running word count: {total_occurrences}")
                
            # Quick 100ms throttle pause to be a courteous crawler
            time.sleep(0.1)
            
        except Exception as e:
            # Silently catch anomalies to prevent a single bad link from blowing up your whole crawl
            continue
            
    # Format a structured data summary to hand back to the LLM model
    result_summary = (
        f"Total Sites Successfully Crawled: {sites_visited_count}\n"
        f"Total Aggregate Occurrences of '{target_word}': {total_occurrences}"
    )
    return result_summary

if __name__ == "__main__":
    # Initialize your model setup
    model = init_chat_model("gpt-5-nano")
    model_with_tools = model.bind_tools([batch_word_occurrences])
    
    messages = [{
        "role": "user", 
        "content": "Analyze the Spring 2026 batch at https://www.ycombinator.com/companies?batch=Spring%202026. Visit each startup's profile page, count the total number of times the word 'agent' appears across all of them, and tell me how many sites were successfully visited."
    }]
    
    print("🤖 Model processing intent...")
    ai_message = model_with_tools.invoke(messages)
    messages.append(ai_message)
    
    if ai_message.tool_calls:
        for tool_call in ai_message.tool_calls:
            # The model automatically extracts "Spring 2026" and "agent" out of your prompt text!
            tool_output = batch_word_occurrences.invoke(tool_call["args"])
            
            tool_message = ToolMessage(
                content=str(tool_output), 
                tool_call_id=tool_call["id"]
            )
            messages.append(tool_message)
            
        print("\n🤖 Processing final synthesis report...")
        final_response = model_with_tools.invoke(messages)
        print("\n" + "="*50)
        print("🎬 ANALYSIS REPORT SUMMARY")
        print("="*50)
        print(final_response.content)
        print("="*50)
    else:
        print(f"\n🤖 Response (No tool execution required): {ai_message.content}")
