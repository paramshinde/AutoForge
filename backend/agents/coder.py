import os
import json
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from core.state import AgentState

llm = ChatGroq(
    model="llama-3.3-70b-versatile", 
    temperature=0,
    api_key=os.getenv("GROQ_API_KEY")
)

def coding_agent_node(state: AgentState):
    iteration = state.get("iterations", 0)
    error_logs = state.get("error_logs", "")
    requirements = state['requirements']
    user_story = state['user_story']
    
    print(f"--- CODING AGENT (Groq): Iteration {iteration} ---")
    
    # SYSTEM PROMPT
    system_message = """You are an expert Web Developer.
    You must output a JSON object with exactly these keys: 
    "html_code", "css_code", "js_code", "backend_code", "database_schema".
    
    1. html_code: The full HTML structure (body content).
    2. css_code: Modern, attractive CSS styling.
    3. js_code: Functional JavaScript logic.
    4. backend_code: A simple FastAPI backend stub.
    
    Ensure the code works together. Do not include markdown formatting."""

    # HUMAN PROMPT (Template)
    if error_logs:
        # Retry Mode
        human_template = """The previous code failed tests.
        Error Log: {error_logs}
        
        Please rewrite the code to fix these errors.
        Original Request: {user_story}
        """
    else:
        # Creation Mode
        human_template = """Create a full solution for this User Story: {user_story}
        
        Detailed Requirements:
        {requirements}
        
        Make the UI modern, clean, and responsive.
        """

    # Create Prompt Template
    prompt = ChatPromptTemplate.from_messages([
        ("system", system_message), 
        ("human", human_template)
    ])
    
    chain = prompt | llm
    
    try:
        # SAFE INVOKE: Pass variables here so curly braces in data don't break LangChain
        response = chain.invoke({
            "user_story": user_story,
            "requirements": str(requirements),
            "error_logs": error_logs
        })
        
        content = response.content.strip()
        # Clean markdown
        if content.startswith("```json"): content = content[7:]
        if content.startswith("```"): content = content[3:]
        if content.endswith("```"): content = content[:-3]
        
        data = json.loads(content, strict=False)
        return {
            "html_code": data.get("html_code", ""),
            "css_code": data.get("css_code", "/* No CSS */"),
            "js_code": data.get("js_code", "// No JS"),
            "backend_code": data.get("backend_code", "# No Backend"),
            "database_schema": data.get("database_schema", "-- No DB"),
            "iterations": iteration + 1
        }
    except Exception as e:
        print(f"Gen Error: {e}")
        return {
            "html_code": f"",
            "iterations": iteration + 1
        }