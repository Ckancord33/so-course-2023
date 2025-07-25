#!/bin/bash

# Iniciar el generador de archivos en background
python3 ./file_generator.py &

# Iniciar la aplicación Flask en foreground
python3 ./app.py