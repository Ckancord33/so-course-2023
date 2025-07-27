from flask import Flask, send_from_directory, jsonify
import os
import requests

# Se crea la aplicación Flask
app = Flask(__name__)

# --- Definir la ruta a las carpetas de archivos ---
PUBLIC_DIR = '/usr/src/app/sync_files/public'
PRIVATE_DIR = '/usr/src/app/sync_files/private'

# --- Obtener la lista de compañeros de la red ---
# Leemos la variable de entorno PEERS que pasamos con docker run
containers_str = os.getenv('CONTAINERS', '')
CONTAINERS = containers_str.split(',') if containers_str else []

# --- Obtener el nombre del contenedor actual ---
ACTUAL_CONTAINER = os.getenv('MY_CONTAINER', '')

# --- Funcion para consultar los archivos publicos de un contenedor ---
def get_container_public_files(container_name):
  """
  Función helper que consulta los archivos públicos de un contenedor específico.
  Retorna una lista de archivos o una lista vacía si hay error.
  """
  try:
    url = f'http://{container_name}:5000/internal/public-files'
    print(f"Consultando al contenedor: {url}")
    response = requests.get(url, timeout=3)
    
    if response.status_code == 200:
      return response.json().get('files', [])
    else:
      print(f"El contenedor {container_name} devolvió un error: {response.status_code}")
      return []
      
  except requests.exceptions.RequestException as e:
    print(f"ERROR: No se pudo conectar con el contenedor '{container_name}'. Motivo: {e}")
    return []

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
    return jsonify({'status': 'success', 'files': files})
  except FileNotFoundError:
    # Manejo de error por si la carpeta no existe
    return jsonify({'status': 'error', 'message': 'El directorio público no fue encontrado.'}), 404

# 2. Endpoint para comprobar si un archivo existe localmente
@app.route('/internal/has-file/<path:filename>')
def has_file(filename):
    """
    Comprueba si un archivo específico existe en la carpeta pública local.
    """
    file_path = os.path.join(PUBLIC_DIR, filename)
    if os.path.exists(file_path):
        return jsonify({'has_file': True})
    else:
        return jsonify({'has_file': False})

# 3. Endpoint para que un peer entregue un archivo a otro peer
@app.route('/internal/get-file/<path:filename>')
def get_file(filename):
    """
    Sirve un archivo desde el directorio público local.
    """
    try:
        # send_from_directory es la forma segura de Flask para enviar archivos
        return send_from_directory(PUBLIC_DIR, filename, as_attachment=True)
    except FileNotFoundError:
        return "Archivo no encontrado", 404

# --- ENDPOINTS DEL PROYECTO (Externos) ---

# 1. Endpoint para listar archivos de un contenedor específico
#    Responde a URLs como: /storage/abcde12345
@app.route('/storage/<uid>')
def list_specific_files(uid):
  """
  Lista los archivos publicos y privados de un contenedor.
  Si la solicitud es del mismo contenedor, incluye archivos privados.
  """
  if uid not in CONTAINERS:
    return jsonify({'message': f'Contenedor {uid} no encontrado en la red.'}), 404
  
  # Obtener archivos públicos
  public_files = get_container_public_files(uid)
  
  # Si no se pudieron obtener los archivos públicos
  if not public_files and uid != ACTUAL_CONTAINER:
    return jsonify({'message': f'No se pudieron obtener los archivos del contenedor {uid}.'}), 503
  
  # Preparar respuesta base
  response_data = {
    'message': f'Archivos del contenedor {uid}',
    'files_publicos': public_files
  }
  
  # Si la solicitud es del mismo contenedor, incluir archivos privados
  if uid == ACTUAL_CONTAINER:
    try:
      private_files = os.listdir(PRIVATE_DIR)
    except FileNotFoundError:
      private_files = []
    
    response_data['files_privados'] = private_files
    response_data['message'] = f'Archivos públicos y privados del contenedor {uid}'
  
  return jsonify(response_data)
    
# 2. Endpoint para listar todos los archivos públicos de la red
#    Responde a la URL: /public/
@app.route('/public/')
def list_public_files():
  """
  Lista todos los archivos de la carpeta 'public' de todos los contenedores.
  """
  all_files = []
  print(f"Coordinador consultando a los contenedores: {CONTAINERS}")

  # Iterar sobre la lista de todos los contenedores en la red
  for container in CONTAINERS:
    files = get_container_public_files(container)
    all_files.extend(files)

  return jsonify({
    'message': 'Agregación de archivos públicos de la red completada.',
    'contenedores_consultados': CONTAINERS,
    'files': all_files
  })

# 3. Endpoint para descargar un archivo
#    Responde a URLs como: /download/mi_archivo.txt
@app.route('/download/<path:name_ext>')
def download_file(name_ext):
  """
  Busca un archivo en toda la red y lo sirve para su descarga.
  Busca archivos públicos en todos los contenedores y archivos privados solo en el contenedor actual.
  """
  print(f"Solicitud de descarga para el archivo: {name_ext}")
  
  # Primero buscar en archivos privados del contenedor actual
  try:
    private_file_path = os.path.join(PRIVATE_DIR, name_ext)
    if os.path.exists(private_file_path):
      print(f"¡Archivo privado encontrado en el contenedor actual!")
      return send_from_directory(PRIVATE_DIR, name_ext, as_attachment=True)
  except Exception as e:
    print(f"Error al buscar en archivos privados: {e}")
  
  # Luego buscar en archivos públicos de todos los contenedores
  for container in CONTAINERS:
    try:
      print(f"Verificando archivos públicos del contenedor '{container}'...")
      
      # 1. Preguntar al contenedor qué archivos públicos tiene
      files = get_container_public_files(container)
      
      # Si el contenedor tiene el archivo en su lista pública
      if name_ext in files:
        print(f"¡Archivo público encontrado en el contenedor '{container}'!")
        
        # 2. Pedirle el archivo directamente al contenedor para servirlo
        download_url = f'http://{container}:5000/internal/get-file/{name_ext}'
        file_response = requests.get(download_url, stream=True, timeout=30)
        
        if file_response.status_code == 200:
          # Devolvemos la respuesta del otro contenedor directamente al usuario
          return file_response.content, file_response.status_code, dict(file_response.headers)
        else:
          print(f"Error al descargar desde {container}: {file_response.status_code}")

    except requests.exceptions.RequestException as e:
      print(f"Error al contactar al contenedor '{container}' para la descarga: {e}")
      continue  # Continuar con el siguiente contenedor

  # Si el bucle termina y no se encontró el archivo
  return jsonify({'status': 'error', 'message': 'Archivo no encontrado en la red.'}), 404

# 4. Endpoint para subir un archivo a un contenedor
#    Responde a URLs como: /upload/abcde12345/nuevo_archivo.txt
#    Nota: Este endpoint necesitará usar el método POST en el futuro.
@app.route('/upload/<uid>/<path:name_ext>')
def upload_file(uid, name_ext):
  """
  Permite subir un archivo a un contenedor específico.
  Por ahora, solo devuelve un mensaje de prueba.
  """


  get_file(name_ext)
  return jsonify({
    'message': f'Aquí se subiría el archivo {name_ext} al contenedor {uid}.'
  })

# --- Endpoint de prueba para la raíz ---
@app.route('/')
def index():
    return jsonify({'message': 'El servidor Synchrontainer está funcionando!'})


# Se asegura de que el servidor sea accesible desde fuera del contenedor
app.run(host='0.0.0.0')
