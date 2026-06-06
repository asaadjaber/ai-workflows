from langchain_ollama import ChatOllama
from langchain_community.tools import DuckDuckGoSearchRun
from langgraph.prebuilt import create_react_agent

# 1. Initialize our local model
# Note: Ensure you pulled the model (e.g., llama3) via Ollama
llm = ChatOllama(model="llama3.1", temperature=0)

# 2. Define the tool the agent is allowed to use
search_tool = DuckDuckGoSearchRun()
tools = [search_tool]

# 3. Create the agent using LangGraph's modern, bulletproof prebuilt engine
# This completely avoids the legacy LangChain agent import issues
agent_executor = create_react_agent(llm, tools)

if __name__ == "__main__":
    competitors = ["Zendesk", "Intercom"]
    
    query = (
        f"Find recent news, major features, or pricing changes for "
        f"{', '.join(competitors)} that a competitor could use as a selling point."
    )
    
    print(f"Starting autonomous research on: {competitors}...\n")
    
    # 4. Invoke the agent graph. 
    # Modern agents expect a list of messages as input.
    inputs = {"messages": [("user", query)]}
    response = agent_executor.invoke(inputs)
    
    # The last message in the returned list contains the final answer
    final_message = response["messages"][-1]
    
    print("\n--- Final Research Report ---")
    print(final_message.content)
