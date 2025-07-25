import random
import time
import os
from datetime import datetime

# --- Configuración ---
# Directorio donde se guardarán los archivos públicos.
# La ruta es relativa a la ubicación del script dentro del contenedor.
PUBLIC_DIR = './sync_files/public'
# Intervalo de espera en segundos
WAIT_INTERVAL = 60

def create_random_file():
  """
  Genera un número aleatorio y lo guarda en un nuevo archivo de texto
  dentro del directorio público.
  """
  try:

    # 1. Generar un número aleatorio entre 1 y 100000
    random_number = random.randint(1, 100000)

    # 2. Crear un nombre de archivo único usando la fecha y hora actual
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_name = f'file_{timestamp}.txt'
    file_path = os.path.join(PUBLIC_DIR, file_name)

    # 3. Escribir el número en el archivo
    with open(file_path, 'w') as f:
        f.write(str(random_number))

    print(f"Archivo creado: {file_path} con el número {random_number}")

  except Exception as e:
    print(f"Error al crear el archivo: {e}")

print("Iniciando el generador de archivos aleatorios...")
while True:
  create_random_file()
  print(f"--- Esperando {WAIT_INTERVAL} segundos para el próximo archivo ---")
  time.sleep(WAIT_INTERVAL)