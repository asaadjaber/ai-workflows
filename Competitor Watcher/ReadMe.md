## Competitor Watcher

This mini-project takes mocked competitor research data and creates embeddings of the data which it puts into a Weaviate collection. The project implements Hypothetical Document Embeddings (HyDE) to ensure that an accurate semantic search is performed. 

# Built with

- Python
- ngrok
- Ollama
- nomic embed text 

# Setup

1. Clone the repository

2. Setup a Python environment 

```bash
python3 -m venv venv
```
```bash
source venv/bin/activate
```
3. Install the required dependencies: 

```bash
pip install weaviate-client
pip install requests
```
Install Ollama:

https://ollama.com/download/mac

4. Open an ngrok tunnel and serve the Ollama instance:
```bash
ngrok http 11434
```
```bash
OLLAMA_HOST=0.0.0.0 /Applications/Ollama.app/Contents/Resources/ollama serve
```
5. Setup project:

Export your weaviate API key and REST Endpoint URL.

Ensure you replace the `NGROK_OLLAMA_ENDPOINT` in `config.py` with the Forwarding URL from ngrok.

6. Run the project:

```bash
python main.py
```

## Sample Output: 

📊 [FINAL COMPETITIVE INTELLIGENCE EXECUTIVE UPDATE]

**Strategic Tactical Response Assessment Recommendation**

**Competitor Analysis:** AlphaCorp's recent pricing update and BetaSystems' technology addition have significant implications for our mid-market pricing strategies.

**Key Takeaways:**

1. **AlphaCorp Pricing Update:** The reduction of Enterprise seat pricing from $150 to $99 per month (with an annual commitment) is a strategic move to attract more customers and increase market share. This change may prompt us to reassess our own pricing structure to remain competitive.
2. **BetaSystems Technology Addition:** Dr. Sarah Jenkins' appointment as Chief Technology Officer brings valuable expertise in core ML infrastructure. This addition may enhance BetaSystems' capabilities, potentially leading to improved product offerings or enhanced customer experiences.

**Recommendation:**

To maintain a competitive edge and align with market trends, we should consider the following strategic tactical responses:

1. **Mid-Market Pricing Review:** Conduct a thorough review of our mid-market pricing strategy to ensure it remains competitive in light of AlphaCorp's pricing update.
2. **Product/Service Enhancement:** Leverage BetaSystems' technology addition by incorporating similar innovations into our own product or service offerings to differentiate ourselves and enhance customer value.
3. **Competitive Intelligence Gathering:** Increase monitoring of AlphaCorp and BetaSystems' developments to stay informed about their strategic moves, allowing us to adjust our strategies accordingly.

**Next Steps:**

1. Schedule a pricing strategy review with senior leadership to assess the impact of AlphaCorp's pricing update on our mid-market offerings.
2. Identify areas where we can enhance our product or service offerings by leveraging BetaSystems' technology addition.
3. Develop a competitive intelligence gathering plan to stay informed about AlphaCorp and BetaSystems' future moves.

By implementing these strategic tactical responses, we can maintain a competitive edge in the market, adapt to changing market conditions, and ultimately drive business growth.
