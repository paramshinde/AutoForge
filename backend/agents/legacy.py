import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq

#llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash-lite", temperature=0)
llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0, api_key=os.getenv("GROQ_API_KEY"))
def legacy_analysis_agent(code_snippet: str):
    """
    Analyzes an existing code snippet to extract architecture.
    """
    print(f"--- LEGACY AGENT: Analyzing {len(code_snippet)} bytes of code ---")

    # --- MOCK MODE (Instant & Safe) ---
    if os.getenv("USE_MOCK_AI", "false").lower() == "true":
        return """
**Architecture Analysis:**
* **Framework:** Python Flask (v2.0+)
* **Database:** SQLite (detected via 'sqlite3' import)
* **Key Endpoints:**
    * `GET /` (Home)
    * `POST /add_user` (User Registration)

**Integration Strategy:**
To add the new 'Login' feature to this legacy app, we should:
1.  Create a new blueprint for Auth.
2.  Use the existing `db_session` for user queries.
3.  Add a generic `User` model that extends the current schema.
        """

    # --- REAL AI MODE ---
    safe_snippet = code_snippet[:2000] # Limit to 2000 chars
    prompt = ChatPromptTemplate.from_template(
        """Analyze this code:
        {code}
        
        Briefly list: Framework, DB, and how to add a Login feature.
        """
    )
    
    chain = prompt | llm
    try:
        # Use the truncated snippet
        response = chain.invoke({"code": safe_snippet})
        return response.content
    except Exception as e:
        return f"Error: {e}"