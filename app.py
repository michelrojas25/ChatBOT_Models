
import gradio as gr
from groq_api import consulta_api_groq  # Importamos la función que consulta la API

# Función de respuesta integrada con la API de Groq
def chat_response(user_input, history):
    if history is None:
        history = []

    # Llamar a la API de Groq para obtener la respuesta
    bot_response = consulta_api_groq(user_input)

    # Actualizar el historial con la consulta y la respuesta
    history.append({"role": "user", "content": user_input})
    history.append({"role": "assistant", "content": bot_response})
    return history, history

# Crear la interfaz con diseño ajustado
with gr.Blocks() as chat_interface:
    # Encabezado principal
    with gr.Row():
        gr.Markdown("## ¿Cmo qué puedo ayudarte?", elem_id="header")

    # Área de conversación con historial
    with gr.Row(elem_id="chat_row"):
        chat_history = gr.Chatbot(label="", type="messages", elem_id="chat_area")

    # Entrada de texto y botones
    with gr.Row(elem_id="input_row"):
        user_input = gr.Textbox(
            placeholder="Envía un mensaje atu ChatBOT",
            show_label=False,
            elem_id="input_box"
        )
        gr.Button("Enviar", elem_id="send_button", variant="primary").click(
            chat_response, inputs=[user_input, gr.State()], outputs=[chat_history, gr.State()]
        )

    # Fila de acciones adicionales con botones funcionales
    with gr.Row(elem_id="actions_row"):
        gr.Button("🖼️ Crea una imagen", elem_id="action_button").click(
            lambda: "Quiero crear una imagen sobre [tema]", inputs=[], outputs=[user_input]
        )
        gr.Button("📝 Resume un texto", elem_id="action_button").click(
            lambda: "Resúmeme el siguiente texto: [texto aquí]", inputs=[], outputs=[user_input]
        )
        gr.Button("📊 Analiza datos", elem_id="action_button").click(
            lambda: "Analiza este conjunto de datos: [datos o contexto]", inputs=[], outputs=[user_input]
        )
        gr.Button("✍️ Ayúdame a escribir", elem_id="action_button").click(
            lambda: "Ayúdame a redactar un texto sobre [tema]", inputs=[], outputs=[user_input]
        )
        gr.Button("➕ Más", elem_id="action_button")  # Este botón puede ser funcional más adelante

# CSS para ajustar el diseño
chat_interface.css = """
body {
    margin: 0;
    padding: 0;
    background-color: #181818; /* Fondo oscuro */
}
#header {
    text-align: center;
    font-size: 24px;
    font-weight: bold;
    margin-top: 250px; /* Baja el encabezado */
    margin-bottom: 20px;
    color: #ffffff;
}
#chat_row, #input_row, #actions_row {
    width: 100%;
    max-width: 800px;
    margin: 0 auto;
}
#chat_area {
    height: 200px;
    max-height: 200px;
    overflow-y: auto;
    border: 1px solid #ccc;
    border-radius: 5px;
    padding: 10px;
    width: 100%;
}
#input_row {
    margin-top: 20px;
    display: flex;
    justify-content: center;
    align-items: center;
}
#input_box { 
    display: flex; 
    align-items: center; 
    justify-content: left; /* O usa center si quieres centrar completamente */
}
#send_button {
    width: 80px; /* Acomoda el tamaño del botón */
    height: 35px; /* Ajusta la altura */
    font-size: 14px; /* Ajusta el tamaño del texto */
    padding: 5px; /* Añade espacio interno */
    text-align: center; /* Centra el texto */
    overflow: hidden; /* Maneja el texto si desborda */
}
#actions_row {
    margin-top: 20px;
    display: flex;
    justify-content: space-around;
}
#action_button {
    font-size: 14px;
    padding: 5px 10px;
    display: flex;
    align-items: center;
    justify-content: center;
}
"""

# Lanzar la interfaz
chat_interface.launch()

