# Funds BTG API (FastAPI)

## Tabla de Contenidos
- [Introducción](#introduction)
- [Características](#features)
- [Instalación](#installation)
- [Uso](#usage)
- [Despliegue](#deployment)

## Introducción
FastAPI es un framework web moderno, rápido (de alto rendimiento) para construir APIs con Python 3.7+ basado en indicaciones de tipo estándar de Python.

## Características
- Alto rendimiento gracias a Starlette y Pydantic.
- Documentación de API interactiva autogenerada (Swagger UI y ReDoc).
- Sistema de inyección de dependencias.
- Manejo de solicitudes asincrónicas.

## Instalación

### Requisitos previos
- Python 3.10+
- Git

### Pasos
1. Clonar el repositorio:
    ```bash
    git clone https://github.com/dagiraldomu/funds_fastApi.git
    cd funds_fastApi
    ```

2. Crear y activar un entorno virtual:
    ```bash
    python -m venv .venv
    source .venv/bin/activate  # En Windows, usar `env\Scripts\activate`
    ```

3. Instalar las dependencias:
    ```bash
    pip install -r requirements.txt
    ```
   
4. Variables de Entorno

Este proyecto requiere algunas variables de entorno para funcionar correctamente. Las variables se cargan desde un archivo `.env`. Por razones de seguridad, el archivo `.env` real no está incluido en el control de versiones.

- Crea un archivo `.env` en la raíz de tu proyecto.
- Copia el contenido de `.env-example` a tu archivo `.env`:

   ```bash
   cp .env-example .env
   ```
  
5. (Opcional) Correr los seeders para poblar la colección con los fondos por defecto 
   ```bash
    python app/seeders/seed_funds.py
    ```
6. (Opcional) Ejecutar Pruebas:

   ```bash
    cd app/
    pytest
    ```
## Uso

### Ejecutando el Servidor de Desarrollo
Para iniciar el servidor de desarrollo, ejecuta:
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```
La API estará disponible en `http://127.0.0.1:8000`.

### Accediendo a la Documentación de la API
- Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`

## Despliegue
### Usando Docker
1. construir la imagen Docker:
    ```bash
    docker build -t app-funds-image .
    ```

2. Ejecutar el contenedor Docker:
    ```bash
    docker run -d --name app-container -p 8000:8000 app-funds-image
    ```

### Desplegando en un Proveedor de la Nube
Consulta la documentación específica del proveedor de nube para desplegar aplicaciones FastAPI (por ejemplo, AWS, Azure, Google Cloud).
