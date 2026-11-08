from __future__ import annotations

import sqlite3
from pathlib import Path

SCHEMA_PATH = Path(__file__).with_name("schema.sql")


def conectar(db_path: str | Path = ":memory:") -> sqlite3.Connection:
    """Abre una conexión SQLite con claves foráneas activas y filas por nombre."""
    conn = sqlite3.connect(str(db_path))
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn


def inicializar_bd(
    conn: sqlite3.Connection,
    schema_path: str | Path = SCHEMA_PATH,
) -> None:
    """Crea las tablas, restricciones e índices definidos en schema.sql."""
    schema = Path(schema_path).read_text(encoding="utf-8")
    conn.executescript(schema)
    conn.commit()


def crear_bd(db_path: str | Path = ":memory:") -> sqlite3.Connection:
    """Atajo: abre la conexión e inicializa el esquema en un solo paso."""
    conn = conectar(db_path)
    inicializar_bd(conn)
    return conn
