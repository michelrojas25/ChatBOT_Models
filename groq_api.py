import os
import requests
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Función para consultar la API de Groq
def consulta_api_groq(prompt, context=None, modelo=None):
    api_key = os.getenv('GROQ_API_KEY')
    if not api_key:
        raise ValueError("No se encontró la API key de Groq")

    # URL base de la API de Groq
    url = "https://api.groq.com/openai/v1/chat/completions"

    # Usar el modelo proporcionado o el predeterminado
    modelo_a_usar = modelo if modelo else "llama3-70b-8192"

    # Preparar los mensajes incluyendo el contexto si existe
    messages = []
    if context:
        messages.extend(context)
    messages.append({"role": "user", "content": prompt})

    # Datos para la solicitud
    data = {
        "model": modelo_a_usar,
        "messages": messages,
        "temperature": 0.7,
        "max_tokens": 2048
    }

    # Cabeceras de la solicitud
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()  # Lanzar excepción si hay error HTTP
        
        if response.status_code != 200:
            print(f"Error API: {response.text}")  # Debug
            raise Exception(f"API error: {response.status_code}")
            
        return response.json()['choices'][0]['message']['content']
    except requests.exceptions.RequestException as e:
        print(f"Error en la solicitud: {str(e)}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"Respuesta de la API: {e.response.text}")
        raise Exception(f"Error al comunicarse con la API de Groq: {str(e)}")

