from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage

# 1. Initialize the local model
llm = ChatOllama(model="llama3.1", temperature=0.7) # Higher temperature for creative email writing!

# 2. Define a prompt template that expects a history of messages
prompt_template = ChatPromptTemplate.from_messages([
    (
        "system",
        "You are an elite Sales Copilot. You are helping an Account Executive draft a "
        "personalized outreach email based on competitive research.\n\n"
        "Here is the research background you must use:\n{research_data}"
    ),
    # This placeholder tells LangChain to dynamically inject the chat history array here
    MessagesPlaceholder(variable_name="chat_history"),
    ("human", "{user_input}")
])

# 3. Create the chain
chat_chain = prompt_template | llm

if __name__ == "__main__":
    # This simulates passing the output from Phase 2 straight into Phase 3
    mock_phase_2_research = """
    1. Zendesk is more customizable but requires more setup.
    2. Zendesk has deeper service reporting; Intercom focuses on conversations.
    3. Zendesk starting price is $19/agent; Intercom is $39/seat.
    """
    
    # This Python list acts as our native memory storage bank
    history = []
    
    print("AI Copilot Initialized. Ask it to draft or refine the email (type 'quit' to exit).\n")
    
    while True:
        user_msg = input("You: ")
        if user_msg.lower() == "quit":
            break
            
        # Run the chain, passing background research, historical messages, and new input
        response = chat_chain.invoke({
            "research_data": mock_phase_2_research,
            "chat_history": history,
            "user_input": user_msg
        })
        
        print(f"\nCopilot: {response.content}\n")
        
        # CRITICAL STEP: Manually append the exchange to our history object
        # This builds the continuous structural memory string behind the scenes
        history.append(HumanMessage(content=user_msg))
        history.append(AIMessage(content=response.content))
