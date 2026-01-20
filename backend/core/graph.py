from langgraph.graph import StateGraph, END
from .state import AgentState

# --- IMPORTS ---
from agents.ado_connector import ado_connector_node
from agents.coder import coding_agent_node 
from agents.tester import testing_agent_node
# 👇 THIS WAS MISSING
from agents.architect import architect_agent_node 

# --- CONDITIONAL LOGIC ---
def should_continue(state: AgentState):
    results = state.get("test_results", "")
    iterations = state.get("iterations", 0)
    
    if "PASS" in results:
        print("--- DECISION: Tests Passed. Finishing. ---")
        return "end"
    
    if iterations < 3:
        print(f"--- DECISION: Tests Failed. Retrying (Attempt {iterations}/3)... ---")
        return "retry"
    
    print("--- DECISION: Max retries reached. Stopping. ---")
    return "end"

# --- WORKFLOW ---
workflow = StateGraph(AgentState)

# Add Nodes
workflow.add_node("ado_connector", ado_connector_node)
workflow.add_node("architect", architect_agent_node) # The new brain
workflow.add_node("coder", coding_agent_node)
workflow.add_node("tester", testing_agent_node)

# Define Edges
workflow.set_entry_point("ado_connector")
workflow.add_edge("ado_connector", "architect") # 1. Connector -> Architect
workflow.add_edge("architect", "coder")         # 2. Architect -> Coder
workflow.add_edge("coder", "tester")            # 3. Coder -> Tester

# Conditional Edge (Self-Healing Loop)
workflow.add_conditional_edges(
    "tester",
    should_continue,
    {
        "end": END,
        "retry": "coder" 
    }
)

app = workflow.compile()