Chatbot de Flores - Asistente Virtual para Consultas Personalizadas


![Logo de Flowershop](https://floreak.es/wp-content/uploads/2024/01/Captura-de-pantalla-2024-01-02-182423-e1707068790441.png "Logo de la Floristería")

Este proyecto es un chatbot inteligente especializado en flores, desarrollado con Python, Streamlit para la interfaz de usuario, Docker para la contenerización, y PostgreSQL gestionado mediante pgAdmin. Está desplegado en Render para un acceso en línea eficiente y escalable.

Características:

Chatbot inteligente para responder preguntas sobre tipos de flores, cuidados, riego, ubicación, entre otros.
Interfaz web amigable creada con Streamlit.
Base de datos PostgreSQL para almacenar información sobre flores y registros de usuarios 
Docker para contenerización y despliegue fácil.
pgAdmin para administración y monitoreo de la base de datos.
Despliegue en Render, listo para producción.

Tecnologías Usadas
Python 
Streamlit
PostgreSQL
pgAdmin 
Docker 
Render.com 

Estructura del Proyecto
bash
Copiar
Editar
chatbot-flores/
│
├── app/                      # Código principal de Streamlit
│   └── main.py               # Interfaz del chatbot
│
├── db/                       
│   ├── init.sql              # Script para inicializar la base de datos
│
├── docker-compose.yml        # Configuración de Docker Compose
├── Dockerfile                # Imagen para el servicio de Streamlit
├── requirements.txt          # Dependencias del proyecto
├── README.md                 # Este archivo

Instrucciones para Ejecutar Localmente
Clona el repositorio:

bash
Copiar
Editar
git clone https://github.com/tuusuario/chatbot-flores.git
cd chatbot-flores
Configura variables de entorno si es necesario.

Construye y levanta los contenedores con Docker Compose:

bash
Copiar
Editar
docker-compose up --build
Accede al chatbot en:
http://localhost:8501

Accede a pgAdmin en:
http://localhost:5050

Despliegue en Render
Render se utiliza para desplegar tanto la app de Streamlit como la base de datos (en modo gestionado o externo).

Subir el proyecto a GitHub.
Conectar el repo a Render.
Configurar los servicios (web y base de datos) desde el dashboard.



Próximas Mejoras:

Soporte para imágenes de flores.

Autenticación de usuarios.

Registro de historial de conversaciones.




Contribuciones
¡Las contribuciones son bienvenidas! Si deseas mejorar el bot o agregar nuevas funciones, crea un fork, haz tus cambios y envía un pull request.




Contacto
¿Dudas o sugerencias?
Escríbeme a: info.anaexposito@gmail.com
