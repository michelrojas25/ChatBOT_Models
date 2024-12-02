import gradio as gr
from groq_api import consulta_api_groq
from chat_storage import AlmacenamientoChat

# Inicializaciones
almacenamiento = AlmacenamientoChat()
id_conversacion_actual = None
chat_history_global = []

# Configuración de modelos disponibles
MODELOS_DISPONIBLES = {
    "Meta": [
        "llama3-8b-8192",
        "llama-3.1-70b-versatile",
        "llama-3.1-8b-instant",
        "llama-3.2-1b-preview",
        "llama-3.2-3b-preview",
        "llama-3.2-11b-vision-preview",
        "llama-3.2-90b-vision-preview",
        "llama-guard-3-8b",
        "llama3-70b-8192"
    ],
    "Google": [
        "gemma-7b-it",
        "gemma2-9b-it"
    ],
    "Groq": [
        "llama3-groq-70b-8192-tool-use-preview",
        "llama3-groq-8b-8192-tool-use-preview"
    ],
    "Mistral AI": [
        "mixtral-8x7b-32768"
    ],
    "OpenAI": [
        "whisper-large-v3",
        "whisper-large-v3-turbo"
    ],
    "Hugging Face": [
        "distil-whisper-large-v3-en"
    ],
    "Otros": [
        "llava-v1.5-7b-4096-preview"
    ]
}

# Función para obtener lista plana de modelos
def get_all_models():
    return [model for provider in MODELOS_DISPONIBLES.values() for model in provider]

def chat_response(user_input, history, modelo_seleccionado):
    global id_conversacion_actual, chat_history_global
    
    # Extraer el nombre real del modelo (eliminar el prefijo del proveedor)
    modelo_real = modelo_seleccionado.split(" - ")[1] if " - " in modelo_seleccionado else modelo_seleccionado
    
    if not user_input.strip():
        return history, history, ""
    
    try:
        # Obtener el contexto del historial
        context = [
            {"role": msg["role"], "content": msg["content"]} 
            for msg in history[-4:] if history
        ]
        
        # Llamar a la API con el modelo seleccionado
        bot_response = consulta_api_groq(
            prompt=user_input,
            context=context,
            modelo=modelo_real
        )
        
        # Actualizar historial
        if history is None:
            history = []
        history.append({"role": "user", "content": user_input})
        history.append({"role": "assistant", "content": bot_response})
        chat_history_global = history
        
    except Exception as e:
        error_message = f"Error con el modelo {modelo_real}: {str(e)}"
        if history is None:
            history = []
        history.append({"role": "user", "content": user_input})
        history.append({"role": "assistant", "content": error_message})
        chat_history_global = history
    
    return history, history, ""

# Interfaz
with gr.Blocks() as chat_interface:
    # Layout principal con dos columnas
    with gr.Row():
        # Columna izquierda (chat)
        with gr.Column(scale=4):
            gr.Markdown("## ¿Cómo puedo ayudarte?", elem_id="header")
            
            chat_history = gr.Chatbot(
                value=chat_history_global,
                label="",
                elem_id="chat_area",
                height=600,
                type="messages"
            )
            
            with gr.Row():
                user_input = gr.Textbox(
                    placeholder="Envía un mensaje...",
                    show_label=False,
                    elem_id="input_box",
                    lines=3
                )
                
            with gr.Row():
                clear_button = gr.Button("️", elem_id="clear_button")
                send_button = gr.Button("Enviar", elem_id="send_button", variant="primary")
        
        # Columna derecha (selector de modelo)
        with gr.Column(scale=1):
            gr.Markdown("### Modelo")
            
            # Dropdown con los modelos organizados por proveedor
            modelo_selector = gr.Dropdown(
                choices=[f"{provider} - {model}" 
                        for provider, models in MODELOS_DISPONIBLES.items()
                        for model in models],
                value="Meta - llama3-70b-8192",  # Modelo por defecto
                label="Selecciona un modelo",
                elem_id="model_selector"
            )

    # Eventos
    send_button.click(
        chat_response,
        inputs=[user_input, gr.State(chat_history_global), modelo_selector],
        outputs=[chat_history, gr.State(), user_input]
    )

    user_input.submit(
        chat_response,
        inputs=[user_input, gr.State(chat_history_global), modelo_selector],
        outputs=[chat_history, gr.State(), user_input]
    )

    clear_button.click(
        lambda: ([], [], ""),
        outputs=[chat_history, gr.State(), user_input]
    )

    # CSS actualizado para incluir el selector de modelos
    chat_interface.css = """
    body {
        margin: 0;
        padding: 0;
        background-color: #1a237e;
    }
    #chat_area {
        height: 600px !important;
        border-radius: 10px;
        background-color: #283593;
        margin: 10px 0;
    }
    #input_box {
        min-height: 60px !important;
        border-radius: 8px;
        background-color: #283593;
        color: #ffffff;
    }
    #model_selector {
        background-color: #283593;
        color: #ffffff;
        border-radius: 8px;
        margin-top: 10px;
    }
    #send_button, #clear_button {
        height: 40px;
        margin: 5px;
    }
    #send_button {
        background-color: #4CAF50;
        color: white;
    }
    #clear_button {
        background-color: #ff4444;
        color: white;
    }
    .message {
        padding: 15px;
        margin: 5px;
        border-radius: 10px;
    }
    .user {
        background-color: #3949ab;
    }
    .bot {
        background-color: #283593;
    }
    """

if __name__ == "__main__":
    chat_interface.launch()

