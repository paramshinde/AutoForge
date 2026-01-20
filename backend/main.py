import os
from dotenv import load_dotenv

# 1. Load environment variables BEFORE importing the graph
load_dotenv()

# Debug check: Print to see if the key is loaded (masked)
key = os.getenv("GOOGLE_API_KEY")
if not key:
    print(" ERROR: GOOGLE_API_KEY not found in environment!")
    print("Make sure you have a .env file with GOOGLE_API_KEY=AIzaSy...")
    exit(1)
else:
    print(f"API Key loaded: {key[:5]}********")

# 2. Now it's safe to import the graph
from core.graph import app

if __name__ == "__main__":
    # Simulate an input from ADO
    initial_input = {"user_story": "As a user, I want a login page so I can access the system."}
    
    print("Starting AutoForge Orchestrator...")
    try:
        result = app.invoke(initial_input)
        print("\n--- FINAL OUTPUT ---")
        print(result)
    except Exception as e:
        print(f"\n Execution Error: {e}")