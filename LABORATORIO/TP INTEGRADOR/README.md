# Trabajo Práctico Integrador - Sistema de Gestión de Tickets

## Descripción general

Sistema de soporte técnico y gestión de tickets desarrollado en **Python 3.10+** con persistencia en **SQLite**. El proyecto implementa una arquitectura por capas, principios **SOLID** y el patrón **Repository**, separando las entidades de negocio, la lógica de persistencia, la orquestación de casos de uso y la interfaz de demostración por consola.

El dominio modela el ciclo de vida completo de un ticket de soporte: creación por parte de un cliente, asignación automática a un técnico según el rubro del producto, intercambio de mensajes mediante hitos cronológicos inmutables, cierre y reapertura con validación de la regla de negocio de los 30 días.

| Aspecto | Detalle |
|---|---|
| Materia | Algoritmos y Estructuras de Datos 3 |
| Modalidad | Laboratorio - Trabajo Práctico Integrador |
| Lenguaje | Python 3.10+ |
| Persistencia | SQLite mediante `sqlite3` de la biblioteca estándar |
| Dependencias externas | Ninguna |
| Patrón principal | Repository + separación por capas |
| Punto de entrada | `main.py` |

### Objetivos del trabajo

- Modelar las entidades del dominio con tipos explícitos y reglas de negocio encapsuladas.
- Aplicar el patrón Repository para desacoplar la lógica de negocio del motor de base de datos.
- Persistir usuarios, clientes, técnicos, productos, tickets e hitos en SQLite con integridad referencial.
- Implementar los flujos de los Diagramas de Secuencia **DS-01**, **DS-02**, **DS-03** y **DS-04**.
- Demostrar el ciclo de vida completo mediante una ejecución interactiva por consola.

---

## Arquitectura del Proyecto y Patrones de Diseño

La aplicación se organiza en capas con dependencias unidireccionales. La interfaz de consola invoca a los controladores, los controladores orquestan el dominio y los repositorios, y la persistencia queda aislada detrás de interfaces abstractas.

```text
┌─────────────────────────────────────────────────────┐
│ main.py / CLI (demostración de casos de uso)        │
└──────────────────────────┬──────────────────────────┘
                           │
┌──────────────────────────▼──────────────────────────┐
│ controllers/ (orquestación de casos de uso)         │
│ ProductoController · TicketController               │
│ HitoController · NotificacionController             │
└──────────────────────────┬──────────────────────────┘
                           │
┌──────────────────────────▼──────────────────────────┐
│ domain/ (entidades, enums y reglas de negocio)      │
│ Usuario · Cliente · Tecnico · Producto              │
│ Ticket · Hito · RubroTipo · EstadoTicket            │
└──────────────────────────▲──────────────────────────┘
                           │
┌──────────────────────────┴──────────────────────────┐
│ repositories/ (interfaces ABC + implementaciones)   │
│ IRepositorioProducto · IRepositorioTicket           │
│ IRepositorioHito · IRepositorioUsuario              │
│ SQLiteProductoRepository · SQLiteTicketRepository   │
│ SQLiteHitoRepository · SQLiteUsuarioRepository      │
└──────────────────────────┬──────────────────────────┘
                           │
┌──────────────────────────▼──────────────────────────┐
│ database.py + schema.sql (conexión y esquema)       │
│ SQLite · PRAGMA foreign_keys = ON · índices         │
└─────────────────────────────────────────────────────┘
```

### `domain/`: modelo de negocio

Contiene las entidades y enumeraciones del UML, sin dependencias de SQLite ni de la consola.

- **`Usuario`**: clase base con `nombre`, `email` e `idUsuario`.
- **`Cliente(Usuario)`**: agrega `telefono`, `direccion` y las operaciones `solicitarCierreTicket()` y `solicitarReaperturaTicket()`.
- **`Tecnico(Usuario)`**: agrega `rubroEspecialidad`, `disponible` y `puedeAtender(rubro)`.
- **`Producto`**: `idProducto`, `nombre`, `marca`, `modelo`, `rubro` y `obtenerRubro()`.
- **`Ticket`**: `idTicket`, `fechaCreacion`, `estado`, `descripcion`, `producto`, `cliente`, `tecnico`, `hitos`, más los métodos `crearTicket(mensaje)` y `cambiarEstado(nuevoEstado)`.
- **`Hito`**: `id`, `mensaje`, `fechaHora`, `autor`. Se implementa como `@dataclass(frozen=True)`, por lo que es **inmutable** una vez creado.
- **Enumeraciones**:
  - `RubroTipo`: `LINEA_BLANCA`, `COCINA`, `ELECTRO`, `PEQUENOS_ELECTRODOMESTICOS`.
  - `EstadoTicket`: `ABIERTO`, `ASIGNADO`, `CERRADO`, `REABIERTO`.

El ticket valida las transiciones de estado permitidas:

| Estado actual | Estados permitidos |
|---|---|
| `ABIERTO` | `ASIGNADO`, `CERRADO` |
| `ASIGNADO` | `ABIERTO`, `CERRADO` |
| `CERRADO` | `REABIERTO` |
| `REABIERTO` | `ASIGNADO`, `CERRADO` |

Si se intenta una transición inválida se lanza `TransicionEstadoInvalidaError`.

> **Decisión de diseño:** se incorporó el atributo auxiliar `fechaCierre` al ticket para poder validar la regla de negocio de reapertura dentro de los 30 días. El resto de los atributos respeta el UML provisto.

### `repositories/`: patrón Repository

La capa de persistencia se define mediante interfaces abstractas con `abc.ABC`:

- `IRepositorioProducto`: `guardar(producto)`, `obtenerPorId(idProducto)`.
- `IRepositorioTicket`: `guardar(ticket)`, `obtenerTicket(idTicket)`, `listarPorCliente(idUsuario)`, `listarPorTecnico(idUsuario)`.
- `IRepositorioHito`: `crear(hito, idTicket)`, `listarPorTicket(idTicket)`.
- `IRepositorioUsuario`: interfaz auxiliar para persistir y reconstruir clientes/técnicos, y para consultar técnicos disponibles. Es necesaria para resolver la asignación automática por rubro y la reconstrucción de objetos de dominio.

Las implementaciones concretas son:

- `SQLiteProductoRepository`
- `SQLiteTicketRepository`
- `SQLiteHitoRepository`
- `SQLiteUsuarioRepository`

**¿Cómo desacopla esto la lógica de negocio del motor de base de datos?** Los controladores dependen únicamente de las interfaces (`IRepositorioTicket`, `IRepositorioProducto`, etc.), nunca de `sqlite3` ni de las clases concretas. Si en el futuro se quisiera migrar a PostgreSQL, MySQL u otro motor, alcanzaría con crear nuevas implementaciones que respeten las mismas interfaces, sin modificar el dominio ni los controladores. Los repositorios SQLite se encargan de traducir entre filas relacionales y objetos de dominio, reconstruyendo productos, clientes, técnicos, tickets e hitos.

### `controllers/`: orquestación de casos de uso

Los controladores coordinan el dominio, los repositorios y las notificaciones:

- **`ProductoController`**: `asignarTipoProducto(idProducto, rubro)` y `obtenerProducto(idProducto)`.
- **`TicketController`**: `crearTicket(...)`, `iniciarAsignacion(...)`, `cambiarEstado(...)`, `cerrarTicket(...)` y `reabrirTicket(...)`.
- **`HitoController`**: `agregarHito(ticket, mensaje, autor)`, persiste el hito y notifica a la contraparte.
- **`NotificacionController`**: `notificarCliente(...)`, `notificarTecnico(...)`, `notificarCierre(ticket)` y `notificarReapertura(ticket)`. En esta demo las notificaciones se emiten por consola y se conservan en un historial.

### `database.py` y `schema.sql`: persistencia SQLite

- `database.py` centraliza la conexión mediante `conectar()`, activa `PRAGMA foreign_keys = ON;`, configura `row_factory = sqlite3.Row` e inicializa el esquema con `inicializar_bd()`.
- `schema.sql` define las tablas relacionales normalizadas:
  - `usuarios`: datos comunes (`idUsuario`, `nombre`, `email`, `tipo`).
  - `clientes`: `telefono`, `direccion`, clave foránea a `usuarios`.
  - `tecnicos`: `rubroEspecialidad`, `disponible`, clave foránea a `usuarios`.
  - `productos`: `nombre`, `marca`, `modelo`, `rubro`.
  - `tickets`: fechas, estado, descripción, claves foráneas a producto, cliente y técnico, más `fechaCierre`.
  - `hitos`: mensaje, fecha/hora, autor y ticket, con claves foráneas.
- Se utilizan restricciones `CHECK` para los enums y la disponibilidad, y se crean índices sobre cliente, técnico, estado, ticket de los hitos y rubros.
- Cada operación de escritura confirma la transacción con `commit()`.

### Principios SOLID aplicados

| Principio | Aplicación en el proyecto |
|---|---|
| **S** - Responsabilidad Única | El dominio modela reglas, los repositorios persisten, los controladores orquestan y `main.py` demuestra. |
| **O** - Abierto/Cerrado | Se pueden agregar nuevas implementaciones de repositorios sin modificar controladores ni dominio. |
| **L** - Sustitución de Liskov | Las implementaciones SQLite son sustituibles por las interfaces abstractas declaradas. |
| **I** - Segregación de Interfaces | Cada agregado tiene una interfaz pequeña y específica (`IRepositorioProducto`, `IRepositorioTicket`, `IRepositorioHito`). |
| **D** - Inversión de Dependencias | Los controladores dependen de abstracciones (`ABC`), no de las clases concretas de SQLite. |

---

## Mapeo y Cobertura de Diagramas de Secuencia (DS)

| Diagrama | Caso de uso | Implementación principal | Resultado esperado |
|---|---|---|---|
| **DS-01** | Creación de ticket | `TicketController.crearTicket()` + `HitoController.agregarHito()` | Ticket en `ABIERTO` con hito inicial persistido |
| **DS-02** | Asignación automática por rubro | `TicketController.iniciarAsignacion()` | Ticket en `ASIGNADO`, técnico ocupado y notificaciones |
| **DS-03** | Registro de hitos / chat | `HitoController.agregarHito()` | Hito inmutable asociado al ticket y notificación a la contraparte |
| **DS-04** | Cierre y reapertura | `TicketController.cerrarTicket()` / `reabrirTicket()` | Ticket en `CERRADO` y luego `REABIERTO`, con validación de 30 días |

### DS-01 - Creación de Ticket

1. El cliente selecciona un producto.
2. Se obtiene el rubro mediante `Producto.obtenerRubro()`.
3. `TicketController.crearTicket()` valida la existencia del producto y del cliente.
4. Se instancia el `Ticket` con estado `EstadoTicket.ABIERTO` y se persiste mediante `IRepositorioTicket.guardar()`.
5. Se genera el hito inicial de creación mediante `HitoController.agregarHito()`, que lo persiste en `IRepositorioHito`.

### DS-02 - Asignación Automática por Rubro

1. `TicketController.iniciarAsignacion(idTicket, rubroTicket)` recupera el ticket.
2. Se consultan los técnicos disponibles con `IRepositorioUsuario.listarTecnicos(soloDisponibles=True)`.
3. Se filtra por especialidad con `Tecnico.puedeAtender(rubroTicket)`.
4. Si no hay candidatos, se lanza `SinTecnicoDisponibleError`.
5. Se asigna el técnico, se cambia el estado a `ASIGNADO`, se marca al técnico como no disponible y se guarda el ticket.
6. Se notifica al cliente con `NotificacionController.notificarCliente()` y se informa al técnico con `notificarTecnico()`.

### DS-03 - Registro de Hitos / Chat

1. `HitoController.agregarHito(ticket, mensaje, autor)` crea un `Hito` inmutable con fecha y hora actuales.
2. El hito se persiste con `IRepositorioHito.crear(hito, idTicket)`.
3. El hito se agrega a la colección `ticket.hitos`.
4. Se notifica a la contraparte:
   - Si el autor es un `Tecnico`, se notifica al `Cliente`.
   - Si el autor es un `Cliente` y el ticket tiene técnico, se notifica al `Tecnico`.
5. Los hitos no se modifican ni se eliminan: son un historial cronológico inmutable.

### DS-04 - Administración de Estados: Cierre y Reapertura

**Cierre:**

1. `TicketController.cerrarTicket(idTicket, autor)` cambia el estado a `CERRADO` y registra `fechaCierre`.
2. Se libera al técnico asignado (`disponible = True`).
3. Se persiste el ticket y se registra un hito de cierre.
4. Se dispara `NotificacionController.notificarCierre(ticket)`.

**Reapertura:**

1. `TicketController.reabrirTicket(idTicket, autor, fechaReferencia=None)` valida que el ticket esté en `CERRADO`.
2. Se calcula el tiempo transcurrido desde `fechaCierre`.
3. Si supera los 30 días, se lanza `ReaperturaFueraDePlazoError`.
4. Si está dentro del plazo, se cambia el estado a `REABIERTO` y se persiste.
5. Se registra el hito de reapertura y, si hay un técnico disponible para el rubro, se reasigna y se marca como ocupado.
6. Se dispara `NotificacionController.notificarReapertura(ticket)`.

La demo incluye una prueba adicional que cierra un segundo ticket e intenta reabrirlo 31 días después, evidenciando el rechazo controlado de la operación.

---

## Estructura de Archivos

```text
TP INTEGRADOR/
├── README.md
├── main.py
├── database.py
├── schema.sql
├── domain/
│   ├── __init__.py
│   ├── enums.py
│   ├── exceptions.py
│   ├── usuario.py
│   ├── producto.py
│   ├── hito.py
│   └── ticket.py
├── repositories/
│   ├── __init__.py
│   ├── interfaces.py
│   ├── sqlite_usuario_repository.py
│   ├── sqlite_producto_repository.py
│   ├── sqlite_hito_repository.py
│   └── sqlite_ticket_repository.py
└── controllers/
    ├── __init__.py
    ├── producto_controller.py
    ├── ticket_controller.py
    ├── hito_controller.py
    └── notificacion_controller.py
```

| Archivo / directorio | Responsabilidad |
|---|---|
| `main.py` | Demostración ejecutable y orquestación de los casos de uso. |
| `database.py` | Conexión SQLite, activación de claves foráneas e inicialización del esquema. |
| `schema.sql` | Definición de tablas, restricciones e índices. |
| `domain/` | Entidades, enumeraciones y reglas de negocio. |
| `repositories/` | Interfaces abstractas e implementaciones SQLite. |
| `controllers/` | Casos de uso, coordinación y notificaciones. |

---

## Requisitos y Ejecución

### Requisitos

- **Python 3.10 o superior**.
- No se requieren dependencias externas: se utiliza únicamente la biblioteca estándar, en particular `sqlite3`, `abc`, `dataclasses`, `datetime` y `argparse`.

Verificación de la versión:

```bash
python --version
```

### Ejecución de la demostración

Desde la raíz del proyecto:

```bash
python main.py
```

Esto crea (o reinicia) el archivo `ticketing.db` en el directorio del proyecto y ejecuta la demostración completa.

Para ejecutar sin generar archivo, usando una base en memoria:

```bash
python main.py --memory
```

También se puede indicar una ruta alternativa para la base:

```bash
python main.py --db ruta/al/archivo.db
```

### ¿Qué realiza `main.py`?

1. **Inicialización:** abre la conexión SQLite, activa `PRAGMA foreign_keys = ON;` y ejecuta `schema.sql` para crear las tablas e índices.
2. **Sembrado inicial:** inserta 1 cliente, 2 técnicos con rubros distintos (`LINEA_BLANCA` y `COCINA`) y 2 productos (heladera y microondas).
3. **DS-01:** crea un ticket para la heladera en estado `ABIERTO`, lo persiste y registra el hito inicial.
4. **DS-02:** busca un técnico disponible para `LINEA_BLANCA`, lo asigna, cambia el estado a `ASIGNADO` y emite notificaciones.
5. **DS-03:** agrega mensajes del técnico y del cliente como hitos inmutables, notificando a la contraparte.
6. **DS-04 cierre:** cambia el ticket a `CERRADO`, registra la fecha de cierre, libera al técnico, guarda el hito y notifica.
7. **DS-04 reapertura:** valida el plazo de 30 días, cambia el estado a `REABIERTO`, reasigna técnico si corresponde y notifica.
8. **Prueba de regla de negocio:** crea y cierra un segundo ticket, e intenta reabrirlo 31 días después para demostrar el rechazo mediante `ReaperturaFueraDePlazoError`.
9. **Consultas:** lista tickets por cliente y por técnico usando `IRepositorioTicket`.
10. **ProductoController:** demuestra `asignarTipoProducto()` cambiando el rubro del segundo producto.
11. **Verificación de integridad:** ejecuta `PRAGMA foreign_key_check` y `PRAGMA integrity_check` e informa el resultado por consola.
12. **Persistencia:** al finalizar, deja los datos almacenados en `ticketing.db` (si no se usó `--memory`).

### Salida esperada (resumen)

La ejecución muestra secciones claramente separadas para cada diagrama y notificaciones con el formato:

```text
[NOTIFICACIÓN -> Cliente María López <maria.lopez@example.com>] Su ticket #1 fue asignado al técnico Carlos Pérez (LINEA_BLANCA).
```

Al finalizar, la verificación esperada es:

```text
PRAGMA foreign_key_check : OK (sin violaciones)
PRAGMA integrity_check   : ok
```

Y el estado persistido esperado es:

```text
Ticket #1: REABIERTO
Ticket #2: CERRADO
Técnico Carlos Pérez (LINEA_BLANCA): ocupado
Técnico Lucía Gómez (COCINA): disponible
```

> **Nota:** en modo archivo, `main.py` elimina cualquier archivo existente en la ruta indicada (por defecto `ticketing.db`) antes de inicializar la demo, para que la ejecución sea idempotente. Si se necesitan conservar datos entre ejecuciones, se debe adaptar el flujo de inicialización de `main.py` o utilizar directamente los controladores y repositorios sin ejecutar la demo.

### Inspección manual de la base

Opcionalmente, se puede abrir la base con la herramienta `sqlite3`:

```bash
sqlite3 ticketing.db ".tables"
sqlite3 ticketing.db "SELECT idTicket, estado, idTecnico FROM tickets;"
sqlite3 ticketing.db "SELECT idTicket, COUNT(*) FROM hitos GROUP BY idTicket;"
```

---

## Resumen de valor académico

El proyecto evidencia la aplicación conjunta de:

- Modelado orientado a objetos con herencia, composición, enumeraciones y encapsulamiento de reglas de negocio.
- Arquitectura por capas con bajo acoplamiento y alta cohesión.
- Patrón Repository con inversión de dependencias mediante interfaces abstractas.
- Persistencia relacional normalizada con integridad referencial y transacciones.
- Implementación trazable de los Diagramas de Secuencia DS-01 a DS-04.
- Validación explícita de reglas de negocio mediante excepciones del dominio.
