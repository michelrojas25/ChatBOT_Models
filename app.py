import gradio as gr
from groq_api import consulta_api_groq
from chat_storage import AlmacenamientoChat

# Inicializamos el almacenamiento y variables globales
almacenamiento = AlmacenamientoChat()
id_conversacion_actual = None
chat_history_global = []  # Variable global para mantener el historial

def chat_response(user_input, history):
    global id_conversacion_actual, chat_history_global
    
    if history is None:
        history = chat_history_global  # Usar el historial global
        if not history:  # Si el historial está vacío, iniciar nueva conversación
            id_conversacion_actual = almacenamiento.iniciar_conversacion("Nueva Conversación")
    
    if not user_input.strip():
        return history, history, ""
    
    try:
        context = [
            {"role": msg["role"], "content": msg["content"]} 
            for msg in history[-4:]
        ]
        
        bot_response = consulta_api_groq(user_input, context=context)
        
        # Guardar en la base de datos
        almacenamiento.guardar_mensaje(id_conversacion_actual, "usuario", user_input)
        almacenamiento.guardar_mensaje(id_conversacion_actual, "asistente", bot_response)
        
        # Actualizar el historial
        history.append({"role": "user", "content": user_input})
        history.append({"role": "assistant", "content": bot_response})
        chat_history_global = history  # Actualizar el historial global
        
    except Exception as e:
        error_message = f"Lo siento, ha ocurrido un error: {str(e)}"
        history.append({"role": "user", "content": user_input})
        history.append({"role": "assistant", "content": error_message})
        chat_history_global = history  # Actualizar el historial global
    
    return history, history, ""

def clear_history():
    global id_conversacion_actual, chat_history_global
    if id_conversacion_actual is not None:
        almacenamiento.eliminar_conversacion(id_conversacion_actual)
        id_conversacion_actual = None
    chat_history_global = []  # Limpiar el historial global
    return None

# Interfaz
with gr.Blocks() as chat_interface:
    # Encabezado
    with gr.Row():
        gr.Markdown("## ¿Cómo puedo ayudarte?", elem_id="header")

    # Chat
    with gr.Row(elem_id="chat_row"):
        chat_history = gr.Chatbot(
            value=chat_history_global,  # Inicializar con el historial global
            label="",
            elem_id="chat_area",
            height=600,
            type="messages"
        )

    # Entrada y botones
    with gr.Row(elem_id="input_row"):
        with gr.Column(scale=20):
            user_input = gr.Textbox(
                placeholder="Envía un mensaje a tu ChatBOT",
                show_label=False,
                elem_id="input_box",
                lines=3
            )
        with gr.Column(scale=1):
            send_button = gr.Button("Enviar", elem_id="send_button", variant="primary")
            clear_button = gr.Button("🗑️", elem_id="clear_button")

    # Configurar eventos
    send_button.click(
        chat_response,
        inputs=[user_input, gr.State(chat_history_global)],  # Pasar el historial global
        outputs=[chat_history, gr.State(), user_input]
    )

    clear_button.click(
        clear_history,
        outputs=[chat_history]
    )

    user_input.submit(
        chat_response,
        inputs=[user_input, gr.State(chat_history_global)],  # Pasar el historial global
        outputs=[chat_history, gr.State(), user_input]
    )

    # CSS con tema azul oscuro
    chat_interface.css = """
    body {
        margin: 0;
        padding: 0;
        background-color: #1a237e;  /* Azul oscuro */
    }
    #header {
        text-align: center;
        color: #ffffff;
        margin: 20px 0;
    }
    #chat_area {
        height: 600px !important;
        border-radius: 10px;
        background-color: #283593;  /* Azul un poco más claro */
        margin: 10px 0;
        overflow-y: auto;
    }
    #input_box {
        min-height: 60px !important;
        border-radius: 8px;
        background-color: #283593;  /* Azul un poco más claro */
        color: #ffffff;
        margin-bottom: 10px;
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
    .gradio-container {
        max-width: 1200px !important;
    }
    .message {
        padding: 15px;
        margin: 5px;
        border-radius: 10px;
    }
    .user {
        background-color: #3949ab;  /* Azul para mensajes de usuario */
    }
    .bot {
        background-color: #283593;  /* Azul para mensajes del bot */
    }
    """

# Lanzar la aplicación
if __name__ == "__main__":
    chat_interface.launch()

