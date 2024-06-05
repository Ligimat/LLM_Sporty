import streamlit as st
from main import bot
import time
from PIL import Image

# Configuración de la página
st.set_page_config(page_title="Chat con entrenador personal", page_icon="🏋️‍♀️")

# Estilo para ocultar la interfaz de usuario no deseada
st.markdown("""
<style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# Creación de columnas para el layout
col1, col2, col3, col4 = st.columns([1, 5, 1, 1])


with col3:
    img2 = Image.open("./img/streamlit1.jpg")
    st.image(img2, use_column_width=True)

with col2:
    st.title("🏋️‍♀️ Chat con entrenador personal")
    st.subheader("¿Necesitas entrenar o una dieta?")

    if st.button("Borrar historial"):
        st.session_state.messages = []
        st.experimental_rerun()

# Inicializa el historial de chat
if "messages" not in st.session_state:
    st.session_state.messages = []

# Mostrar mensajes del historial en la recarga de la app
for message in st.session_state.messages:
    avatar = "🏋️" if message["role"] == "user" else "🤖"
    with st.chat_message(message["role"], avatar=avatar):
        st.markdown(message["content"])

# Aceptar entrada del usuario
if prompt := st.chat_input("Ingresa tu consulta..."):
    # Añadir mensaje del usuario al historial del chat
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Mostrar mensaje del usuario en el contenedor del mensaje de chat
    with st.chat_message("user", avatar="🏋️"):
        st.markdown(prompt)

    chat_history = [{"role": "user", "content": message["content"]} for message in st.session_state.messages if message["role"] == "user"]

    # Mostrar respuesta del asistente en el contenedor del mensaje de chat
    with st.chat_message("assistant", avatar="🤖"):
        message_placeholder = st.empty()
        full_response = ""
        

        assistant_response = bot(prompt, chat_history)
        

        # Formatear la respuesta completa antes de procesarla
        formatted_response = assistant_response.replace("### ", "\n🔸 ").replace("\n\n", "\n")

        # Directamente usar markdown para preservar los saltos de línea y el formato
        message_placeholder.markdown(formatted_response, unsafe_allow_html=True)
        
        full_response = formatted_response

    st.session_state.messages.append({"role": "assistant", "content": full_response})

# Botón de navegación que recarga la página
with col4:
    button_text = "Volver"
    target_url = "http://127.0.0.1:5000/inicio.html"
    st.markdown(f'<a href="{target_url}" target="_self" onclick="window.location.reload(true);">{button_text}</a>', unsafe_allow_html=True)
