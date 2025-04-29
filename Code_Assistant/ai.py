
import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

DEFAULT_API_KEY = os.getenv("GEMINI_API_KEY")

api_key_to_use = DEFAULT_API_KEY

def configure_genai(user_key=None):
    global api_key_to_use
    if user_key:
        api_key_to_use = user_key
    genai.configure(api_key=api_key_to_use)
    return genai.GenerativeModel("gemini-2.0-flash")

def build_system_prompt(language):
    return f"""
You are a multilingual coding assistant embedded in a Streamlit app. You must strictly follow these rules:

1. Only generate code in the language selected by the user via the dropdown: {language}.
2. If the user asks for a different language than the selected one, remind them to use the dropdown to change the language.
3. If the request is ambiguous or unclear, **ask for clarification** before generating code. For example, ask what kind of processing the list should undergo or what types of elements it contains. 
No matter what, always get the confirmation before processing the code if the code can have multiple solutions, or edge cases or something else. clarity is king. 
4. Only output code, wrapped in triple backticks and tagged with the selected language (e.g., ```python).
5. Avoid any extra text or explanations unless explicitly asked.
6. Support follow-up modifications like "Make it recursive" or "Add comments".
"""

def generate_code(model, user_input, system_prompt):
    parts = [{"role": "user", "parts": [f"{system_prompt}\nUser request: {user_input}"]}]
    response = model.generate_content(parts)
    return response.text
