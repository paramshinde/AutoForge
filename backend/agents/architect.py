import os
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from core.state import AgentState

llm = ChatGroq(
    model="llama-3.3-70b-versatile", 
    temperature=0.3, # Slightly creative to expand ideas
    api_key=os.getenv("GROQ_API_KEY")
)

def architect_agent_node(state: AgentState):
    print("--- ARCHITECT AGENT: Refining Requirements ---")
    user_story = state['user_story']
    
    # Prompt: Act like a Senior Tech Lead
    system_message = """You are a Senior Solutions Architect.
    Your job is to take a vague User Story and convert it into a detailed technical specification for a Developer.
    
    1. Add specific UI/UX details (colors, layout, responsiveness).
    2. Define the exact HTML structure and CSS classes needed.
    3. Specify the JavaScript logic required.
    4. Keep it concise but comprehensive.
    """
    
    human_message = f"User Story: {user_story}"
    
    prompt = ChatPromptTemplate.from_messages([("system", system_message), ("human", human_message)])
    chain = prompt | llm
    
    try:
        response = chain.invoke({})
        refined_prompt = response.content
        print(f"Refined Spec: {refined_prompt[:100]}...") # Log first 100 chars
        
        # We overwrite the 'requirements' in the state with this super-detailed version
        return {"requirements": [refined_prompt]} 
    except Exception as e:
        print(f"Architect Error: {e}")
        return {"requirements": [user_story]} # Fallback to original