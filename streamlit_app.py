import streamlit as st
import requests
import json
import os

# URL de tu backend Flask (cuando esté desplegado o en local)
# Asegúrate de que coincida con el host y puerto de tu app.py
FLASK_API_URL = os.environ.get("FLASK_API_URL", "http://localhost:5000")

st.set_page_config(page_title="Chatbot de Flores", page_icon="🌸")

st.title("🌸 Tu experta en flores") # Título con emoji de flor
st.markdown("Pregúntame cualquier cosa sobre flores: tipos, cuidados, significado, etc.")

# Inicializar el historial del chat si no existe
if "messages" not in st.session_state:
    st.session_state.messages = []
    # Mensaje de bienvenida del bot
    st.session_state.messages.append({"role": "bot", "content": "Bienvenid@ al mundo de las flores! Soy tu experta floral. ¿Qué te gustaría explorar hoy?"})

# Mostrar mensajes del historial
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Campo de entrada para la pregunta del usuario
if prompt := st.chat_input("Escribe tu pregunta aquí..."):
    # Añadir la pregunta del usuario al historial
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Llamar al backend de Flask
    try:
        # Aquí se hace la solicitud POST a tu API de Flask
        response = requests.post(f"{FLASK_API_URL}/ask", json={"query": prompt})
        response.raise_for_status() # Lanza un error para códigos de estado HTTP 4xx/5xx
        
        bot_response = response.json().get("response", "Lo siento, no pude obtener una respuesta.")
    except requests.exceptions.ConnectionError:
        bot_response = "Error: No se pudo conectar con el servidor del chatbot. Asegúrate de que el backend de Flask esté corriendo."
    except requests.exceptions.HTTPError as e:
        bot_response = f"Error HTTP: {e.response.status_code} - {e.response.text}"
    except Exception as e:
        bot_response = f"Ocurrió un error inesperado: {e}"

    # Añadir la respuesta del bot al historial
    st.session_state.messages.append({"role": "bot", "content": bot_response})
    with st.chat_message("bot"):
        st.markdown(bot_response)