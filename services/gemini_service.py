import os
import json
import google.generativeai as genai
from utils.prompts import WORKOUT_PROMPT, DIET_PROMPT, CHAT_PROMPT, INSIGHTS_PROMPT

def configure_gemini():
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key or api_key == "your_gemini_api_key_here":
        raise ValueError("GEMINI_API_KEY not found or invalid in .env")

    genai.configure(api_key=api_key)

    return genai.GenerativeModel("gemini-2.5-flash")

def parse_json_response(response_text):
    try:
        # Strip markdown json block tags if present
        if response_text.startswith("```json"):
            response_text = response_text[7:]
        if response_text.endswith("```"):
            response_text = response_text[:-3]
        return json.loads(response_text.strip())
    except json.JSONDecodeError as e:
        raise ValueError(f"Failed to parse Gemini response as JSON: {e}\nRaw Response: {response_text}")

def generate_workout_plan(user_data: dict) -> dict:
    model = configure_gemini()
    prompt = WORKOUT_PROMPT.format(**user_data)
    response = model.generate_content(prompt)
    return parse_json_response(response.text)

def generate_meal_plan(user_data: dict) -> dict:
    model = configure_gemini()
    prompt = DIET_PROMPT.format(**user_data)
    response = model.generate_content(prompt)
    return parse_json_response(response.text)

def fitness_chat(user_id, message, chat_history):
    model = configure_gemini()
    # Format history for Gemini
    formatted_history = []
    for msg in chat_history:
        formatted_history.append({"role": msg.role, "parts": [msg.message]})
    
    # Prepend system instructions context if history is empty
    if not formatted_history:
        formatted_history.append({"role": "user", "parts": [CHAT_PROMPT]})
        formatted_history.append({"role": "model", "parts": ["Understood. I am ready to be your fitness coach!"]})
        
    chat = model.start_chat(history=formatted_history)
    response = chat.send_message(message)
    return response.text

def generate_weekly_insights(progress_data: str) -> dict:
    model = configure_gemini()
    prompt = INSIGHTS_PROMPT.format(progress_data=progress_data)
    response = model.generate_content(prompt)
    return parse_json_response(response.text)
