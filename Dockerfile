# Usa una imagen base de Python ligera
FROM python:3.9-slim-buster

# Establece el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copia el archivo de requisitos e instálalos
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia el resto de tu aplicación al directorio de trabajo
COPY . .

# Expone el puerto en el que Flask se ejecutará
EXPOSE 5000

# Comando para ejecutar la aplicación Flask usando Gunicorn
# Gunicorn es un servidor WSGI recomendado para Flask en producción.
# -b 0.0.0.0:5000: Escucha en todas las interfaces en el puerto 5000
# app:app: Indica a Gunicorn que ejecute la aplicación 'app' desde el módulo 'app.py'
CMD ["gunicorn", "-b", "0.0.0.0:5000", "app:app"]