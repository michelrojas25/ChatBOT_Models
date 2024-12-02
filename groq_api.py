import os
import requests
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Función para consultar la API de Groq
def consulta_api_groq(user_input, context=None):
    url = "https://api.groq.com/openai/v1/chat/completions"
    api_key = os.getenv('GROQ_API_KEY')
    
    if not api_key:
        raise ValueError("No se encontró la clave API de Groq. Verifica tus variables de entorno.")
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    
    # Preparar los mensajes con contexto
    messages = []
    if context:
        messages.extend([
            {"role": msg["role"], "content": msg["content"]} 
            for msg in context
        ])
    
    messages.append({"role": "user", "content": user_input})
    
    payload = {
        "model": "llama3-8b-8192",
        "messages": messages,
        "temperature": 0.7,  # Ajustar creatividad
        "max_tokens": 1000   # Ajustar longitud de respuesta
    }

    try:
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        response.raise_for_status()
        
        data = response.json()
        bot_response = data["choices"][0]["message"]["content"]
        return bot_response.strip()
        
    except requests.exceptions.Timeout:
        return "Lo siento, la solicitud ha tardado demasiado tiempo. Por favor, intenta de nuevo."
    except requests.exceptions.RequestException as e:
        return f"Error al consultar la API: {str(e)}"

