import requests
import json
from app import app

class AIService:
    def __init__(self):
        self.gemini_api_key = app.config.get('GEMINI_API_KEY')
        self.base_url = "https://generativelanguage.googleapis.com/v1beta/models/"
        self.text_model = "gemini-1.5-flash-latest"
    
    def call_gemini_api(self, payload, max_retries=3):
        url = f"{self.base_url}{self.text_model}:generateContent?key={self.gemini_api_key}"
        
        for attempt in range(max_retries):
            try:
                response = requests.post(url, json=payload, timeout=30)
                if response.status_code == 200:
                    return response.json()
                elif response.status_code in [503, 500]:
                    if attempt < max_retries - 1:
                        continue
                    else:
                        raise Exception("Service unavailable after retries")
                else:
                    raise Exception(f"API error: {response.status_code}")
            except requests.exceptions.RequestException as e:
                if attempt < max_retries - 1:
                    continue
                else:
                    raise e
        
        raise Exception("Max retries exceeded")

def analyze_plant_image(image_base64, mime_type, language):
    ai_service = AIService()
    
    language_name = 'Malayalam' if language == 'ml-IN' else 'English'
    prompt = f"""Analyze the image of the plant and provide the output in the following strict format. Respond entirely in {language_name}. Use these exact labels (translated to the target language) followed by a colon and a space.

Plant Name: [Identified Plant Name]
Condition: [Healthy/Diseased/Pest Infestation]
Disease/Pest Found: [Name of the disease or pest, or "None"]
Suggested Treatment/Care: [Provide a detailed, step-by-step plan for treatment if a disease is found. If the plant is healthy, provide general care tips including watering, sunlight, and soil requirements.]"""

    payload = {
        "contents": [{
            "parts": [
                {"text": prompt},
                {"inline_data": {"mime_type": mime_type, "data": image_base64}}
            ]
        }]
    }
    
    result = ai_service.call_gemini_api(payload)
    return result['candidates'][0]['content']['parts'][0]['text']

def get_ai_response(conversation, user_message):
    ai_service = AIService()
    
    # Get conversation history
    messages = conversation.messages.order_by('timestamp').all()
    
    # Format history for Gemini API
    formatted_history = []
    for msg in messages:
        role = "user" if msg.sender == "user" else "model"
        formatted_history.append({
            "role": role,
            "parts": [{"text": msg.content}]
        })
    
    # Add current user message
    formatted_history.append({
        "role": "user",
        "parts": [{"text": user_message}]
    })
    
    system_prompt = """You are 'Agri-Assistant', a specialized AI expert in agriculture. Your sole purpose is to provide information and answer questions related to agriculture. This includes topics like crop cultivation, soil science, pest and disease management, agricultural machinery, farming techniques, government agricultural policies, subsidies, market prices for crops, and sustainable farming practices. You MUST STRICTLY adhere to this domain. If a user asks any question not related to agriculture, you must politely and concisely refuse. Respond in the same language as the user's query."""

    payload = {
        "contents": formatted_history,
        "system_instruction": {"parts": [{"text": system_prompt}]}
    }
    
    result = ai_service.call_gemini_api(payload)
    return result['candidates'][0]['content']['parts'][0]['text']

def generate_chat_title(user_message):
    ai_service = AIService()
    
    prompt = f"""Generate a very short title (4-5 words max) for a chat conversation that starts with this user query. Respond with only the title. Query: "{user_message}" """
    
    payload = {
        "contents": [{"parts": [{"text": prompt}]}]
    }
    
    result = ai_service.call_gemini_api(payload)
    title = result['candidates'][0]['content']['parts'][0]['text'].strip().replace('"', '').replace("'", "")
    return title[:50]  # Limit title length

def generate_recommendations(chat_history):
    ai_service = AIService()
    
    summary_prompt = f"""Analyze this agricultural chat history and create a concise "User Interest Profile" summarizing their main interests, crops, problems, and curiosities.

CHAT HISTORY:
{chat_history}"""

    summary_payload = {"contents": [{"parts": [{"text": summary_prompt}]}]}
    summary_result = ai_service.call_gemini_api(summary_payload)
    user_profile = summary_result['candidates'][0]['content']['parts'][0]['text']

    recommendation_prompt = f"""Based on this user profile, provide 3-5 actionable, personalized agricultural recommendations in Markdown format.

USER PROFILE:
{user_profile}"""

    recommendation_payload = {"contents": [{"parts": [{"text": recommendation_prompt}]}]}
    recommendation_result = ai_service.call_gemini_api(recommendation_payload)
    return recommendation_result['candidates'][0]['content']['parts'][0]['text']