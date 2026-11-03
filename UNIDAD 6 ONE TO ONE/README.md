# Unidad 6: Backend con Python - REST API (Flask, SQLite y SQLAlchemy)

Este proyecto implementa una API RESTful con persistencia relacional en SQLite,
utilizando Flask y Connexion para el manejo de rutas y documentación interactiva Swagger (OpenAPI), 
junto con SQLAlchemy como ORM y Marshmallow para la serialización y deserialización de datos.

## 🛠️ Tecnologías utilizadas

- **Python 3**
- **Flask**: Framework web para la construcción del backend.
- **Connexion & Swagger UI**: Especificación OpenAPI y documentación interactiva.
- **SQLite 3**: Base de datos relacional serverless local (`people.db`).
- **Flask-SQLAlchemy**: Mapeo Objeto-Relacional (ORM) para la persistencia de datos.
- **Flask-Marshmallow**: Serialización de objetos Python a JSON.
- **Uvicorn / A2WSGI**: Servidor ASGI de ejecución.

## 📁 Estructura del proyecto

- `config.py`: Configuración e inicialización de Flask, Connexion, SQLAlchemy y Marshmallow.
- `models.py`: Definición del modelo relacional `Person` y el esquema `PersonSchema`.
- `people.py`: Controladores con operaciones CRUD (Create, Read, Update, Delete).
- `app.py`: Entrada principal del servidor y renderizado de la vista home.
- `swagger.yml`: Definición de endpoints de la API REST.
- `people.db`: Base de datos SQLite con la tabla `person`.
- `templates/home.html`: Plantilla HTML para listar personas desde el backend.

## 🚀 Instalación y Ejecución Local

1. **Crear y activar el entorno virtual:**
   ```bash
   python -m venv venv
   .\venv\Scripts\Activate.ps1
1-Instalar dependencias necesarias:
pip install "connexion[flask,swagger-ui,uvicorn]" "flask-marshmallow[sqlalchemy]"
2-Ejecutar la aplicación:
python app.py
3-Acceso:

Frontend: http://localhost:8000/

Swagger UI: http://localhost:8000/api/ui
