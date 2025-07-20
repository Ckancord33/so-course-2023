# imagen base
FROM python:3
# establece el directorio de trabajo
WORKDIR /usr/src/app
# Crear las carpetas para la sincronización de archivos
RUN mkdir -p sync_files/public sync_files/private
# Copiar la carpeta myapp a /usr/src/app
COPY ./myapp/ .
# instalacion de requerimientos y dependencias
RUN pip3 install -r requirements.txt
# Aperturo el puerto 5000 del contenedor
EXPOSE 5000
# Establece el entrypoint
CMD ["python3", "./app.py"]
