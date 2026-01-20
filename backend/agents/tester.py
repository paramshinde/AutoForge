import os
import sys
import subprocess
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from core.state import AgentState

# Initialize Groq
llm = ChatGroq(
    model="llama-3.3-70b-versatile", 
    temperature=0, 
    api_key=os.getenv("GROQ_API_KEY")
)

def testing_agent_node(state: AgentState):
    print("--- TESTING AGENT: Generating & Running Tests ---")

    backend_code = state.get("backend_code", "")
    # The Coder has already incremented this to 1 on the first run.
    

    # --- REAL AI MODE (First Run) ---
    # This runs on the first try, which we expect to FAIL.
    prompt = ChatPromptTemplate.from_template(
        """Write a Python 'unittest' for this code:
        {code}
        Output ONLY raw Python code. No markdown."""
    )
    
    chain = prompt | llm
    try:
        response = chain.invoke({"code": backend_code})
        test_code = response.content.replace("```python", "").replace("```", "")
        
        workspace = "temp_workspace"
        os.makedirs(workspace, exist_ok=True)
        
        with open(f"{workspace}/app.py", "w") as f:
            f.write(backend_code)
        with open(f"{workspace}/test_app.py", "w") as f:
            f.write(test_code)
            
        print("--- TESTING AGENT: Executing Real Tests... ---")
        result = subprocess.run(
            ["python", "test_app.py"], 
            cwd=workspace, 
            capture_output=True, 
            text=True
        )
        
        if result.returncode == 0:
            # If Groq accidentally writes perfect code, we accept it.
            return {"test_results": f"PASS\n{result.stderr}", "error_logs": "", "is_complete": True}
        else:
            # FAILURE (This is what we want for the video story!)
            print(f" REAL TESTS FAILED. Sending feedback to Coder...")
            return {"test_results": f"FAIL\n{result.stderr}", "error_logs": result.stderr, "is_complete": False}

    except Exception as e:
        return {"test_results": f"FAIL: Execution Error - {str(e)}", "error_logs": str(e), "is_complete": False}