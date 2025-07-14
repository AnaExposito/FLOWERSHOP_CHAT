from flask import Flask, request, jsonify
import os
from dotenv import load_dotenv
from flask_cors import CORS

# --- Importaciones para LLM (Groq y Langchain) ---
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# Carga las variables de entorno del archivo .env
load_dotenv()


app = Flask(__name__)

@app.route('/')
def index():
    return "¡Flask está activo!"

# Configuración de la aplicación (cargará desde config.py)
app.config.from_object('config.Config')

CORS(app) # Habilita CORS para todas las rutas

# --- Configuración del LLM de Groq ---
# Asegúrate de que tu GROQ_API_KEY esté en el archivo .env
groq_api_key = os.environ.get("GROQ_API_KEY")
if not groq_api_key:
    raise ValueError("La variable de entorno GROQ_API_KEY no está configurada. Por favor, añádela a tu archivo .env")

# Inicializa el modelo de Groq
# Puedes elegir otros modelos de Groq como "llama3-70b-8192" o "mixtral-8x7b-32768"
llm = ChatGroq(model="llama3-8b-8192", groq_api_key=groq_api_key)

# Define el PromptTemplate usando Langchain
# Esto le da al LLM un contexto y un rol específico
prompt = ChatPromptTemplate.from_messages([
    ("system", "Eres un experto bot de flores. Respondes preguntas sobre tipos de flores, sus cuidados, su significado, su historia y curiosidades. Responde de forma amigable, concisa y útil. Si no sabes la respuesta, di que no lo sabes."),
    ("user", "{query}")
])

# Crea la cadena de Langchain: prompt -> llm -> parser
# El parser convierte la salida del LLM en una cadena de texto simple
chain = prompt | llm | StrOutputParser()

# Ruta para manejar las preguntas del usuario (POST)
@app.route('/ask', methods=['POST'])
def ask_chatbot():
    """
    Recibe la pregunta del usuario, la envía al LLM de Groq
    y devuelve la respuesta generada.
    """
    try:
        user_query = request.json.get('query')

        if not user_query:
            return jsonify({"error": "No se proporcionó ninguna pregunta."}), 400

        # --- Lógica de interacción con el LLM ---
        # Invoca la cadena de Langchain con la pregunta del usuario
        # Esto enviará la pregunta a Groq y obtendrá la respuesta
        llm_response = chain.invoke({"query": user_query})

        # TODO: En FASE 3, aquí se guardará la consulta y la respuesta en la base de datos.
        # save_interaction_to_db(user_query, llm_response)

        # Devuelve la respuesta del LLM al frontend
        return jsonify({"response": llm_response}), 200

    except Exception as e:
        print(f"Se ha producido un error en /ask: {e}")
        return jsonify({"error": f"Se ha producido un error interno: {e}"}), 500

# Esto permite ejecutar la aplicación directamente con `python app.py`
# Para producción, se recomienda usar un servidor WSGI como Gunicorn.
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

