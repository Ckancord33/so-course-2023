import random
import time
import os
from datetime import datetime

# --- Configuración ---
# Directorios donde se guardarán los archivos
PUBLIC_DIR = './sync_files/public'
PRIVATE_DIR = './sync_files/private'
# Intervalo de espera en segundos
WAIT_INTERVAL = 60
# Boolean para alternar entre directorios (True = público, False = privado)
is_public = True
# Nombre del contenedor (se obtiene de la variable MY_CONTAINER que pasamos en docker run)
CONTAINER_NAME = os.getenv('MY_CONTAINER', 'container_unknown')

def create_random_file():
  """
  Genera un número aleatorio y lo guarda en un nuevo archivo de texto.
  Alterna entre directorio público y privado usando un boolean.
  """
  global is_public
  
  try:
    # 1. Generar un número aleatorio entre 1 y 100000
    random_number = random.randint(1, 100000)

    # 2. Crear un nombre de archivo único usando la fecha y hora actual
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # 3. Alternar entre directorio público y privado usando boolean
    if is_public:
      # Boolean True -> directorio público
      directory = PUBLIC_DIR
      dir_type = "PÚBLICO"
      type_name = "public"
    else:
      # Boolean False -> directorio privado
      directory = PRIVATE_DIR
      dir_type = "PRIVADO"
      type_name = "private"
    
    # 4. Formato: contenedor_tipo_fecha.txt
    file_name = f'{CONTAINER_NAME}_{type_name}_{timestamp}.txt'
    file_path = os.path.join(directory, file_name)

    # 5. Crear el directorio si no existe
    os.makedirs(directory, exist_ok=True)

    # 6. Escribir el número en el archivo
    with open(file_path, 'w') as f:
        f.write(f"Número aleatorio: {random_number}\n")
        f.write(f"Tipo: {dir_type}\n")
        f.write(f"Contenedor: {CONTAINER_NAME}\n")
        f.write(f"Creado: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

    print(f"Archivo {dir_type} creado: {file_path} con el número {random_number}")
    
    # Alternar el boolean para la próxima vez
    is_public = not is_public

  except Exception as e:
    print(f"Error al crear el archivo: {e}")

print("Iniciando el generador de archivos aleatorios...")
while True:
  create_random_file()
  print(f"--- Esperando {WAIT_INTERVAL} segundos para el próximo archivo ---")
  time.sleep(WAIT_INTERVAL)