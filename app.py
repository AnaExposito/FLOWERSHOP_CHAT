from flask import Flask, request, jsonify
import os
from dotenv import load_dotenv
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy # Nueva importación
from datetime import datetime # Nueva importación

# --- Importaciones para LLM (Groq y Langchain) ---
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# Carga las variables de entorno del archivo .env
load_dotenv()

app = Flask(__name__)

# Configuración de la aplicación (cargará desde config.py)
app.config.from_object('config.Config')

# Inicializa SQLAlchemy
db = SQLAlchemy(app) # Nuevo

# --- Definición del Modelo de Base de Datos ---
class ChatInteraction(db.Model): # Nuevo
    id = db.Column(db.Integer, primary_key=True)
    user_query = db.Column(db.Text, nullable=False)
    bot_response = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<ChatInteraction {self.id}>'

@app.route('/')
def index():
    return "¡Flask está activo!"

CORS(app) # Habilita CORS para todas las rutas

# --- Configuración del LLM de Groq ---
groq_api_key = os.environ.get("GROQ_API_KEY")
if not groq_api_key:
    raise ValueError("La variable de entorno GROQ_API_KEY no está configurada. Por favor, añádela a tu archivo .env")

llm = ChatGroq(model="llama3-8b-8192", groq_api_key=groq_api_key)

prompt = ChatPromptTemplate.from_messages([
    ("system", "Eres un experto bot de flores. Respondes preguntas sobre tipos de flores, sus cuidados, su significado, su historia y curiosidades. Responde de forma amigable, concisa y útil. Si no sabes la respuesta, di que no lo sabes."),
    ("user", "{query}")
])

chain = prompt | llm | StrOutputParser()

# Ruta para manejar las preguntas del usuario (POST)
@app.route('/ask', methods=['POST'])
def ask_chatbot():
    """
    Recibe la pregunta del usuario, la envía al LLM de Groq
    y devuelve la respuesta generada, guardando la interacción en la DB.
    """
    try:
        user_query = request.json.get('query')

        if not user_query:
            return jsonify({"error": "No se proporcionó ninguna pregunta."}), 400

        llm_response = chain.invoke({"query": user_query})

        # --- Guardar la interacción en la base de datos --- (Modificación FASE 3)
        try:
            new_interaction = ChatInteraction(user_query=user_query, bot_response=llm_response)
            db.session.add(new_interaction)
            db.session.commit()
            print("Interacción guardada en la base de datos.")
        except Exception as db_e:
            # No queremos que un fallo al guardar en DB impida que el usuario reciba la respuesta
            print(f"Error al guardar la interacción en la base de datos: {db_e}")
            # Considera logear esto de alguna otra forma en un entorno de producción

        return jsonify({"response": llm_response}), 200

    except Exception as e:
        print(f"Se ha producido un error en /ask: {e}")
        return jsonify({"error": f"Se ha producido un error interno: {e}"}), 500

# Esta parte del código ya no es necesaria si usas gunicorn para producción
# y en desarrollo puedes ejecutarla directamente.
if __name__ == '__main__':
    # Para la primera ejecución o para desarrollo local, puedes crear las tablas
    # con este bloque. En un entorno de producción con Docker, se gestiona mejor
    # con comandos de Dockerfile o scripts de entrada.
    with app.app_context():
        db.create_all() # Crea las tablas si no existen
    app.run(debug=True, host='0.0.0.0', port=5000)