import os
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate

# Initialize Groq
llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0,
    api_key=os.getenv("GROQ_API_KEY")
)

def legacy_analysis_agent(code_snippet: str):
    """
    Analyzes legacy code to extract architecture and suggest modernization.
    """
    print("--- LEGACY AGENT: Analyzing Codebase ---")
    
    system_message = """You are a Senior Software Architect specializing in Legacy Modernization.
    Analyze the provided code snippet and output a report covering:
    1. **Architecture Detection:** Identify frameworks, languages, and database patterns (e.g., "Monolithic Flask app with SQLite").
    2. **Code Quality Assessment:** List potential issues (security, scalability, maintenance).
    3. **Modernization Strategy:** Suggest how to integrate this into a modern microservices architecture (e.g., "Refactor to FastAPI", "Containerize with Docker").
    
    Keep the output concise and professional, using Python comments (#) format.
    """
    
    human_message = f"Analyze this legacy code:\n\n{code_snippet}"
    
    prompt = ChatPromptTemplate.from_messages([("system", system_message), ("human", human_message)])
    chain = prompt | llm
    
    try:
        response = chain.invoke({})
        return response.content
    except Exception as e:
        return f"# Error analyzing legacy code: {str(e)}"