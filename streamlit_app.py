import streamlit as st
import requests
import json
import os


FLASK_API_URL = os.environ.get("FLASK_API_URL", "https://flowershop-chat.onrender.com")

st.set_page_config(page_title="Chatbot de Flores", page_icon="🌸")

st.title("🌸 Tu experta en flores")
st.markdown("Pregúntame cualquier cosa sobre flores: tipos, cuidados, significado, etc.")


if "messages" not in st.session_state:
    st.session_state.messages = []

    st.session_state.messages.append({"role": "bot", "content": "Bienvenid@ al mundo de las flores! Soy tu experta floral. ¿Qué te gustaría explorar hoy?"})


for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


if prompt := st.chat_input("Escribe tu pregunta aquí..."):

    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)


    try:
   
        response = requests.post(f"{FLASK_API_URL}/ask", json={"query": prompt})
        response.raise_for_status() 
        
        bot_response = response.json().get("response", "Lo siento, no pude obtener una respuesta.")
    except requests.exceptions.ConnectionError:
        bot_response = "Error: No se pudo conectar con el servidor del chatbot. Asegúrate de que el backend de Flask esté corriendo y la URL sea correcta."
    except requests.exceptions.HTTPError as e:
        bot_response = f"Error HTTP: {e.response.status_code} - {e.response.text}"
    except Exception as e:
        bot_response = f"Ocurrió un error inesperado: {e}"


    st.session_state.messages.append({"role": "bot", "content": bot_response})
    with st.chat_message("bot"):
        st.markdown(bot_response)

