# Unidad 6.2: Python Backend con SQLite y Connexion

Implementación de API RESTful en Python utilizando Flask, Connexion (OpenAPI 3.0), SQLAlchemy y Marshmallow con persistencia real en base de datos SQLite.

## Dominio de Datos
Se implementó el dominio de **Clientes (Customers)** como alternativa personalizada a la entidad base:
- `id`: Identificador numérico autoincremental (Clave primaria).
- `fname`: Nombre de pila.
- `lname`: Apellido (identificador único de búsqueda en ruta).
- `email`: Correo electrónico único.
- `phone`: Teléfono de contacto.
- `timestamp`: Marca temporal de creación/modificación generada en UTC.

## Endpoints CRUD Implementados
- `GET /api/customers`: Lista todos los clientes registrados.
- `POST /api/customers`: Da de alta un nuevo cliente.
- `GET /api/customers/{lname}`: Obtiene el detalle de un cliente por apellido.
- `PUT /api/customers/{lname}`: Actualiza los datos de un cliente existente.
- `DELETE /api/customers/{lname}`: Elimina un cliente de la base de datos.

## Documentación Interactiva
La documentación Swagger UI se encuentra disponible en:
- `http://localhost:8000/api/ui`

## Instalación y Ejecución
1. Activar el entorno virtual:
   ```powershell
   .\venv\Scripts\Activate.ps1