import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load the .env file
load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    print("Error: GOOGLE_API_KEY not found in environment.")
else:
    genai.configure(api_key=api_key)
    print(f"Checking models for key ending in: ...{api_key[-4:]}")
    print("--- AVAILABLE MODELS ---")
    try:
        # List all models available to your specific key
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                print(f"Model Name: {m.name}")
    except Exception as e:
        print(f"Error connecting to Google: {e}")