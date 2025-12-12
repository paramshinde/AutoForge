import os
import re
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from core.state import AgentState

llm = ChatGroq(
    model="llama-3.3-70b-versatile", 
    temperature=0,
    api_key=os.getenv("GROQ_API_KEY")
)

def parse_with_delimiters(text):
    """
    Robust parser that extracts code blocks using delimiters.
    This bypasses JSON parsing errors completely.
    """
    data = {}
    
    # Define patterns to extract content between delimiters
    patterns = {
        "html_code": r"---HTML---(.*?)---END_HTML---",
        "css_code": r"---CSS---(.*?)---END_CSS---",
        "js_code": r"---JS---(.*?)---END_JS---",
        "backend_code": r"---BACKEND---(.*?)---END_BACKEND---",
        "database_schema": r"---DB---(.*?)---END_DB---"
    }
    
    for key, pattern in patterns.items():
        match = re.search(pattern, text, re.DOTALL)
        if match:
            data[key] = match.group(1).strip()
        else:
            data[key] = "" # Default to empty if missing
            
    return data

def coding_agent_node(state: AgentState):
    iteration = state.get("iterations", 0)
    error_logs = state.get("error_logs", "")
    requirements = state['requirements']
    user_story = state['user_story']
    
    print(f"--- CODING AGENT (Groq): Iteration {iteration} ---")
    
    # SYSTEM PROMPT: Use delimiters instead of JSON
    system_message = """You are an expert Web Developer.
    You must output the code using the following EXACT format.
    Do not use JSON. Do not use markdown blocks.
    
    ---HTML---
    (Write the index.html code here)
    ---END_HTML---
    
    ---CSS---
    (Write the style.css code here)
    ---END_CSS---
    
    ---JS---
    (Write the script.js code here)
    ---END_JS---
    
    ---BACKEND---
    (Write the main.py FastAPI code here)
    ---END_BACKEND---
    
    ---DB---
    (Write the schema.sql code here)
    ---END_DB---
    """

    if error_logs:
        # RETRY MODE
        human_template = f"""The previous code failed tests.
        Error Log: {error_logs}
        
        Please rewrite the code to fix these errors.
        Original Request: {user_story}
        """
    else:
        # CREATION MODE
        human_template = f"""Create a full solution for this User Story: {user_story}
        
        Requirements:
        {requirements}
        
        Make the UI modern, clean, and responsive.
        """

    prompt = ChatPromptTemplate.from_messages([
        ("system", system_message), 
        ("human", human_template)
    ])
    
    chain = prompt | llm
    
    try:
        # Pass raw strings to avoid variable injection issues
        response = chain.invoke({
            "user_story": user_story,
            "requirements": str(requirements),
            "error_logs": error_logs
        })
        
        content = response.content.strip()
        
        # USE ROBUST PARSER
        data = parse_with_delimiters(content)
        
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