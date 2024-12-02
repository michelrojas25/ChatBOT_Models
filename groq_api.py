import requests

# Función para consultar la API de Groq
def consulta_api_groq(user_input):
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer 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"
    }
    payload = {
        "model": "llama3-8b-8192",
        "messages": [
            {"role": "user", "content": user_input}
        ]
    }

    try:
        # Realizar la solicitud
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()  # Lanza un error si la solicitud falla

        # Procesar la respuesta
        data = response.json()
        bot_response = data["choices"][0]["message"]["content"]
        return bot_response.strip()

    except requests.exceptions.RequestException as e:
        return f"Error al consultar la API: {e}"

