from langgraph.graph import StateGraph, END
from .state import AgentState
from agents.ado_connector import ado_connector_node
from agents.coder import coding_agent_node 
from agents.tester import testing_agent_node

# --- CONDITIONAL LOGIC ---
def should_continue(state: AgentState):
    """
    Decides if we should finish or go back to coding.
    """
    results = state.get("test_results", "")
    iterations = state.get("iterations", 0)
    
    # If tests PASSED, we are done
    if "PASS" in results:
        print("--- DECISION: Tests Passed. Finishing. ---")
        return "end"
    
    # If tests FAILED but we have tried less than 3 times, retry
    if iterations < 3:
        print(f"--- DECISION: Tests Failed. Retrying (Attempt {iterations}/3)... ---")
        return "retry"
    
    # If we failed too many times, give up
    print("--- DECISION: Max retries reached. Stopping. ---")
    return "end"

# --- WORKFLOW ---
workflow = StateGraph(AgentState)

workflow.add_node("ado_connector", ado_connector_node)
workflow.add_node("coder", coding_agent_node)
workflow.add_node("tester", testing_agent_node)

workflow.set_entry_point("ado_connector")
workflow.add_edge("ado_connector", "coder")
workflow.add_edge("coder", "tester")

# THE ADVANCED LOOP:
workflow.add_conditional_edges(
    "tester",
    should_continue,
    {
        "end": END,
        "retry": "coder"  # Go back to Coder!
    }
)

app = workflow.compile()