from flask import Flask

# Se crea la aplicación Flask
app = Flask(__name__)

# --- ENDPOINTS DEL PROYECTO ---

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
