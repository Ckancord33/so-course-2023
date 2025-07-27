#!/bin/bash

# Limpiar contenedores existentes
docker stop contenedor1 contenedor2 2>/dev/null
docker rm contenedor1 contenedor2 2>/dev/null

# Crear red si no existe
docker network create synchrontainer-network 2>/dev/null

# Construir imagen
docker build -t synchrontainer .

# Configurar contenedores
CONTAINERS="contenedor1,contenedor2"

# Lanzar contenedores
docker run -d --name contenedor1 --network synchrontainer-network -p 5000:5000 -e CONTAINERS=$CONTAINERS -e MY_CONTAINER=contenedor1 synchrontainer
docker run -d --name contenedor2 --network synchrontainer-network -p 5001:5000 -e CONTAINERS=$CONTAINERS -e MY_CONTAINER=contenedor2 synchrontainer
