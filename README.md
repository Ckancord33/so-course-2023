# Synchrontainer 🚀

## Resumen del Proyecto

**Synchrontainer** es un sistema de archivos distribuido que utiliza una red de contenedores Docker. El objetivo principal es crear un sistema donde múltiples nodos (contenedores) puedan almacenar archivos y colaborar para compartir información a través de la red.

Cada contenedor en el sistema es un nodo autónomo que:
1.  Puede generar y almacenar sus propios archivos en carpetas `públicas` (compartidas) y `privadas` (locales).
2.  Ejecuta una pequeña aplicación web (un API) que le permite comunicarse con los usuarios y con los otros contenedores.

El sistema permite listar los archivos de un contenedor específico, listar todos los archivos públicos de toda la red, y descargar o subir archivos.

---

## Comandos e Instrucciones Básicas

A continuación se encuentran los pasos esenciales para levantar y ejecutar un nodo (contenedor) de Synchrontainer.

### 1. Crear la Imagen de Docker

La imagen de Docker es el "plano" o la plantilla para nuestros contenedores. Contiene el sistema operativo, el código de Python y todas las dependencias necesarias. Para construir la imagen a partir del `Dockerfile`, sitúate en la carpeta raíz del proyecto y ejecuta:

```bash
docker build -t synchro-app .
```
---

## 2. 🚀 Lanzar un Contenedor

Una vez creada la imagen, podemos lanzar tantos contenedores (nodos) como queramos. Para lanzar un contenedor, usa el siguiente comando:

```bash
docker run -d -p 8081:5000 --name contenedor1 synchro-app
```

- **`docker run`**: El comando para crear y ejecutar un contenedor a partir de una imagen.
- **`-d`**: Ejecuta el contenedor en modo *"detached"* (en segundo plano), para que no ocupe tu terminal.
- **`-p 8081:5000`**: Esta es la parte clave para acceder desde `localhost`.  
  Le dice a Docker:  
  > Toma las peticiones que lleguen al puerto `8081` de mi computadora (localhost)  
  > y reenvíalas al puerto `5000` dentro del contenedor.  

  Gracias a esto, puedes abrir tu navegador y visitar `http://localhost:8081`  
  para comunicarte con la aplicación que corre dentro del contenedor.
- **`--name contenedor1`**: Le da un nombre único al contenedor para poder identificarlo fácilmente.
- **`synchro-app`**: El nombre de la imagen que queremos usar para crear el contenedor.

---

## 🗂 Estructura del Proyecto

### 📁 Carpeta `myapp`

Esta carpeta contiene todo el código fuente de nuestra aplicación escrita en Python:

- **`app.py`**: Es el corazón de la aplicación.  
  Contiene el servidor web creado con la librería Flask.  
  Aquí se define toda la lógica para responder a las peticiones.

- **`requirements.txt`**: Es una lista de todas las librerías de Python que nuestro proyecto necesita para funcionar (como Flask).  
  El `Dockerfile` usa este archivo para instalar las dependencias automáticamente.

---

## 🔗 ¿Qué son los *Endpoints*?

Un **endpoint** es una URL específica que nuestra aplicación `app.py` sabe cómo responder.  
Piensa en ellos como diferentes *servicios* que ofrece nuestro servidor. Por ejemplo:

- **`/public/`**: Es un endpoint que, cuando lo visitas, activa una función en Python  
  para listar todos los archivos públicos de la red.

- **`/download/<nombre_archivo>`**: Es otro endpoint que activa una función  
  para buscar y entregar un archivo específico.

Cada endpoint se define en el código con un decorador como este:

```python
@app.route("/public/")
def listar_publicos():
    ...
```

Ese decorador le dice a Flask:

> "Cuando alguien visite esta URL, ejecuta esta función".

## Comandos que vas a ejecutar mucho

- Construir la imagen

```bash
docker build -t synchrontainer .
```

- Crear la network de docker

```bash
docker network create synchrontainer-network
```

- Crear un contenedor

```bash
CONTAINERS="contenedor1,contenedor2"
docker run -d --name contenedor1 --network synchrontainer-network -p 5000:5000 -e CONTAINERS=$CONTAINERS -e MY_CONTAINER=contenedor1 synchrontainer
docker run -d --name contenedor2 --network synchrontainer-network -p 5001:5000 -e CONTAINERS=$CONTAINERS -e MY_CONTAINER=contenedor2 synchrontainer
```

## 🚀 Despliegue Automático

Para hacer el proceso más rápido y evitar repetir comandos, se incluye un script de bash que automatiza todo el proceso:

### Script `deploy.sh`

Primero dale permisos de ejecución al script:

```bash
chmod +x deploy.sh
```

Luego ejecuta el script:

```bash
./deploy.sh
```

Este script realiza automáticamente todos los pasos necesarios:

1. **Limpia el entorno**: Detiene y elimina contenedores existentes con los mismos nombres
2. **Crea la red Docker**: Configura la red `synchrontainer-network` si no existe
3. **Construye la imagen**: Genera una nueva imagen `synchrontainer` con los cambios más recientes
4. **Lanza los contenedores**: Crea y ejecuta ambos contenedores con toda la configuración necesaria

**Ventajas del script:**
- ✅ Reinicia completamente el sistema con una sola línea
- ✅ Siempre usa la versión más reciente del código
- ✅ No necesitas recordar todos los comandos Docker
- ✅ Evita errores de configuración manual