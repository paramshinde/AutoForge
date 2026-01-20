from typing import TypedDict, List, Optional

class AgentState(TypedDict):
    user_story: str
    requirements: List[str]
    
    # NEW: Broken down Frontend
    html_code: Optional[str]
    css_code: Optional[str]
    js_code: Optional[str]
    
    # Backend & DB remain the same
    backend_code: Optional[str]
    database_schema: Optional[str]
    
    # Validation & Logic
    test_results: Optional[str]
    error_logs: Optional[str]
    iterations: int
    is_complete: bool