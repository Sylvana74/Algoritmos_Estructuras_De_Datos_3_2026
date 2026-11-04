# Unidad 6: Trabajo Práctico Flask - API REST (One-to-Many)

Repositorio de prácticas de laboratorio para la materia **Algoritmos y Estructuras de Datos 3**.

Este proyecto implementa una API RESTful desarrollada con **Python** y **Flask**, gestionando modelos de datos con una relación de uno a muchos (*One-to-Many*).

---

## 📁 Estructura del Proyecto


UNIDAD 6 TP FLASK/
└── rp_flask_api_one_to_many/    # Código fuente de la aplicación Flask
    ├── models/                  # Modelos de base de datos (relación 1:N)
    ├── routes/ o app.py         # Endpoints y lógica de la API
    └── requirements.txt         # Dependencias del proyecto
🛠️ Tecnologías Utilizadas
-Python 3

-Flask

-Flask-SQLAlchemy / SQLite (Mapeo objeto-relacional y persistencia)

-Flask-Marshmallow (Serialización y esquemas de datos)

🚀 Instalación y Puesta en Marcha
1-Clonar o acceder al directorio del proyecto:
cd "LABORATORIO/UNIDAD 6 TP FLASK/rp_flask_api_one_to_many"

2-Crear y activar un entorno virtual:
# En Windows
python -m venv venv
venv\Scripts\activate

3-Instalar dependencias:
pip install -r requirements.txt

4-Ejecutar la aplicación:
flask run
# o bien: python app.py
La API quedará escuchando en http://127.0.0.1:5000/.

📌 Endpoints Principales
Método	 Endpoint	          Descripción
GET     	/api/...	        Listar registros
POST	    /api/...          Crear nuevo registro
GET	      /api/.../<id>	    Obtener detalle por ID
PUT	      /api/.../<id>	    Actualizar un registro
DELETE	  /api/.../<id>	    Eliminar un registro

```text
