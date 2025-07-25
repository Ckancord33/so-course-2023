# imagen base
FROM python:3
# establece el directorio de trabajo
WORKDIR /usr/src/app
# Copiar la carpeta myapp a /usr/src/app
COPY ./myapp/ .
# Crear las carpetas para la sincronización de archivos
RUN mkdir -p sync_files/public sync_files/private
# Dar permisos de ejecución al script de inicio
RUN chmod +x start.sh
# instalacion de requerimientos y dependencias
RUN pip3 install -r requirements.txt
# Aperturo el puerto 5000 del contenedor
EXPOSE 5000
# Establece el entrypoint
CMD ["./start.sh"]
