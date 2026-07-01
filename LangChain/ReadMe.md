# YCombinator Word Crawler

I built an agent that takes a Y-Combinator batch (e.g. Spring 2026) and fetches the list of companies for that batch, then counts the occurences of the word "agent" on that company profile's page including strings such as "agents" or "agentic" and returns the number of sites visited and the occurrences of the word. This agent uses LangChain manual tools to call a `batch_word_occurrences` function that fetches the list of companies and calculates the occurrence of the word "agent" in it. 

## Built With 

- Python
- LangChain Tools
- gpt-5-nano

## Set up

1. Clone the repository.

2. Set up Python environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

3. Export your Open AI API Key: 
```bash
export OPENAI_API_KEY="api-key-here"
```

4. Install required dependencies:
```bash
pip install langchain-core langchain-openai beautifulsoup4 requests
```

5. Run the file:
```bash
ycombinator_crawler.py
```

## Sample Results

🎬 ANALYSIS REPORT SUMMARY
Here are the results for the Spring 2026 batch analysis:

- Total sites successfully visited: 197
- Total aggregate occurrences of the word 'agent' across all visited profiles: 1155

If you’d like, I can break this down per startup (e.g., a list of each profile URL with its individual 'agent' count) or export the data to CSV.

  
