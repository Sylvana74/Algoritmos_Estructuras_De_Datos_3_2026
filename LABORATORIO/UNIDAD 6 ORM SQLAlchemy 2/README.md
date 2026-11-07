# Unidad 6: SQLAlchemy ORM

Implementación práctica de conceptos de mapeo objeto-relacional (ORM) en Python utilizando la sintaxis moderna de **SQLAlchemy 2.0+** sobre bases de datos SQLite locales.

## Contenido de la entrega

1. **`1_crud_basico.py`**:
   - Definición del modelo base `DeclarativeBase` y entidad `User` con tipado estricto (`Mapped`, `mapped_column`).
   - Operaciones CRUD completas: Inserción (`add_all`), consulta y filtrado (`select`, `scalars`), actualización de atributos y eliminación (`delete`).

2. **`2_one_to_many.py`**:
   - Modelado de relación Uno a Muchos entre `User` (padre/autor) y `Post` (hijo/artículo).
   - Uso de clave foránea `ForeignKey("users.id")`.
   - Navegación bidireccional con `relationship(..., back_populates=...)` y cascada completa `cascade="all, delete-orphan"`.

3. **`3_many_to_many.py`**:
   - Modelado de relación Muchos a Muchos entre `Post` (artículo) y `Tag` (etiqueta).
   - Tabla de asociación intermedia (`post_tag_association`) con claves foráneas compuestas.
   - Vinculación cruzada mediante el parámetro `secondary` y manipulación directa de listas en memoria (`append`, `extend`, `remove`).

## Requisitos y Ejecución
- Python 3.10+
- `pip install sqlalchemy`

Ejecución individual:
```powershell
python 1_crud_basico.py
python 2_one_to_many.py
python 3_many_to_many.py