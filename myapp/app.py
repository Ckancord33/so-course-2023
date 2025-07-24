from flask import Flask
import os

# Se crea la aplicación Flask
app = Flask(__name__)

# --- Definir la ruta a las carpetas de archivos ---
PUBLIC_DIR = '/usr/src/app/sync_files/public'

# --- ENDPOINTS INTERNOS ---

# 1. Este endpoint devuelve todos los archivos publicos del contenedor
# es para que los contenedores se pregunten entre sí por sus archivos públicos.
@app.route('/internal/public-files')
def list_own_public_files():
  """
  Lista los archivos que se encuentran en la carpeta 'public' de este contenedor.
  """
  try:
    # os.listdir() devuelve una lista con los nombres de los archivos en la ruta
    files = os.listdir(PUBLIC_DIR)
    return {'status': 'success', 'files': files}
  except FileNotFoundError:
    # Manejo de error por si la carpeta no existe
    return {'status': 'error', 'message': 'El directorio público no fue encontrado.'}, 404

# --- ENDPOINTS DEL PROYECTO (Externos) ---

# 1. Endpoint para listar archivos de un contenedor específico
#    Responde a URLs como: /storage/abcde12345
@app.route('/storage/<uid>')
def list_specific_files(uid):
  """
  Lista los archivos publicos y privados de un contenedor.
  Por ahora, solo devuelve un mensaje de prueba.
  """
  return {
    'message': f'Aquí se mostrarán los archivos del contenedor con ID: {uid}'
  }

# 2. Endpoint para listar todos los archivos públicos de la red
#    Responde a la URL: /public/
@app.route('/public/')
def list_public_files():
  """
  Lista todos los archivos de la carpeta 'public' de todos los contenedores.
  Por ahora, solo devuelve un mensaje de prueba.
  """
  return {
    'message': 'Aquí se mostrarán todos los archivos públicos de la red.'
  }

# 3. Endpoint para descargar un archivo
#    Responde a URLs como: /download/mi_archivo.txt
@app.route('/download/<path:name_ext>')
def download_file(name_ext):
  """
  Permite la descarga de un archivo específico.
  Por ahora, solo devuelve un mensaje de prueba.
  """
  # El <path:..> permite que el nombre del archivo incluya puntos y barras en la variable
  return {
    'message': f'Aquí comenzaría la descarga del archivo: {name_ext}'
  }

# 4. Endpoint para subir un archivo a un contenedor
#    Responde a URLs como: /upload/abcde12345/nuevo_archivo.txt
#    Nota: Este endpoint necesitará usar el método POST en el futuro.
@app.route('/upload/<uid>/<path:name_ext>')
def upload_file(uid, name_ext):
  """
  Permite subir un archivo a un contenedor específico.
  Por ahora, solo devuelve un mensaje de prueba.
  """
  return {
    'message': f'Aquí se subiría el archivo {name_ext} al contenedor {uid}.'
  }

# --- Endpoint de prueba para la raíz ---
@app.route('/')
def index():
    return {'message': 'El servidor Synchrontainer está funcionando!'}


# Se asegura de que el servidor sea accesible desde fuera del contenedor
app.run(host='0.0.0.0')
