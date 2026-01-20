import json
from core.state import AgentState

def ado_connector_node(state: AgentState):
    """
    Simulates fetching a User Story from an ADO export file.
    """
    print("--- ADO CONNECTOR: Reading User Story ---")
    
    # In a real app, this would be an API call to Azure DevOps.
    # For the prototype, we assume the input state already contains the story 
    # or we load a default one.
    
    story = state.get('user_story')
    
    if not story:
        story = "As a HR manager, I want an 'Add Employee' form so that I can record new hires in the system."
    
    # Simple logic to derive requirements (in real life, an LLM would do this too)
    requirements = [
        f"Analyze story: {story}",
        "Frontend: Create a form with fields (Name, Email, Role)",
        "Backend: Create a POST endpoint to receive data",
        "Database: Create an 'employees' table"
    ]
    
    return {
        "user_story": story,
        "requirements": requirements
    }