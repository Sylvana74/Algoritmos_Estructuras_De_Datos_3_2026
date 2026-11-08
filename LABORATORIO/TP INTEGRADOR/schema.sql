PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS usuarios (
    idUsuario INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre    TEXT NOT NULL,
    email     TEXT NOT NULL UNIQUE,
    tipo      TEXT NOT NULL CHECK (tipo IN ('USUARIO', 'CLIENTE', 'TECNICO'))
);

CREATE TABLE IF NOT EXISTS clientes (
    idUsuario INTEGER PRIMARY KEY,
    telefono  TEXT NOT NULL,
    direccion TEXT NOT NULL,
    FOREIGN KEY (idUsuario) REFERENCES usuarios(idUsuario) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS tecnicos (
    idUsuario          INTEGER PRIMARY KEY,
    rubroEspecialidad  TEXT NOT NULL CHECK (rubroEspecialidad IN (
        'LINEA_BLANCA',
        'COCINA',
        'ELECTRO',
        'PEQUENOS_ELECTRODOMESTICOS'
    )),
    disponible         INTEGER NOT NULL DEFAULT 1 CHECK (disponible IN (0, 1)),
    FOREIGN KEY (idUsuario) REFERENCES usuarios(idUsuario) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS productos (
    idProducto INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre     TEXT NOT NULL,
    marca      TEXT NOT NULL,
    modelo     TEXT NOT NULL,
    rubro      TEXT NOT NULL CHECK (rubro IN (
        'LINEA_BLANCA',
        'COCINA',
        'ELECTRO',
        'PEQUENOS_ELECTRODOMESTICOS'
    ))
);

CREATE TABLE IF NOT EXISTS tickets (
    idTicket       INTEGER PRIMARY KEY AUTOINCREMENT,
    fechaCreacion  TEXT NOT NULL,
    estado         TEXT NOT NULL CHECK (estado IN ('ABIERTO', 'ASIGNADO', 'CERRADO', 'REABIERTO')),
    descripcion    TEXT NOT NULL,
    idProducto     INTEGER NOT NULL,
    idCliente      INTEGER NOT NULL,
    idTecnico      INTEGER,
    fechaCierre    TEXT,
    FOREIGN KEY (idProducto) REFERENCES productos(idProducto),
    FOREIGN KEY (idCliente)  REFERENCES clientes(idUsuario),
    FOREIGN KEY (idTecnico)  REFERENCES tecnicos(idUsuario)
);

CREATE TABLE IF NOT EXISTS hitos (
    idHito    INTEGER PRIMARY KEY AUTOINCREMENT,
    mensaje   TEXT NOT NULL,
    fechaHora TEXT NOT NULL,
    idAutor   INTEGER NOT NULL,
    idTicket  INTEGER NOT NULL,
    FOREIGN KEY (idAutor)  REFERENCES usuarios(idUsuario),
    FOREIGN KEY (idTicket) REFERENCES tickets(idTicket) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_tickets_cliente ON tickets(idCliente);
CREATE INDEX IF NOT EXISTS idx_tickets_tecnico ON tickets(idTecnico);
CREATE INDEX IF NOT EXISTS idx_tickets_estado  ON tickets(estado);
CREATE INDEX IF NOT EXISTS idx_hitos_ticket    ON hitos(idTicket);
CREATE INDEX IF NOT EXISTS idx_productos_rubro ON productos(rubro);
CREATE INDEX IF NOT EXISTS idx_tecnicos_rubro  ON tecnicos(rubroEspecialidad, disponible);
