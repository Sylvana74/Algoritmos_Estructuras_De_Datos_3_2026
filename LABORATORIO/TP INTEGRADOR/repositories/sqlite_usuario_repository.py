from __future__ import annotations

import sqlite3

from domain.enums import RubroTipo
from domain.usuario import Cliente, Tecnico, Usuario
from repositories.interfaces import IRepositorioUsuario

_USUARIO_SELECT = """
SELECT u.idUsuario        AS idUsuario,
       u.nombre           AS nombre,
       u.email            AS email,
       u.tipo             AS tipo,
       c.telefono         AS telefono,
       c.direccion        AS direccion,
       t.rubroEspecialidad AS rubroEspecialidad,
       t.disponible       AS disponible
  FROM usuarios u
  LEFT JOIN clientes c ON c.idUsuario = u.idUsuario
  LEFT JOIN tecnicos t ON t.idUsuario = u.idUsuario
"""


class SQLiteUsuarioRepository(IRepositorioUsuario):
    def __init__(self, conn: sqlite3.Connection) -> None:
        self._conn = conn

    def guardar(self, usuario: Usuario) -> Usuario:
        cursor = self._conn.cursor()
        tipo = self._tipo_de(usuario)

        if usuario.idUsuario is None:
            cursor.execute(
                "INSERT INTO usuarios (nombre, email, tipo) VALUES (?, ?, ?)",
                (usuario.nombre, usuario.email, tipo),
            )
            idUsuario = int(cursor.lastrowid)
        else:
            cursor.execute(
                "UPDATE usuarios SET nombre = ?, email = ?, tipo = ? WHERE idUsuario = ?",
                (usuario.nombre, usuario.email, tipo, usuario.idUsuario),
            )
            idUsuario = usuario.idUsuario

        if isinstance(usuario, Cliente):
            cursor.execute(
                """
                INSERT INTO clientes (idUsuario, telefono, direccion)
                VALUES (?, ?, ?)
                ON CONFLICT(idUsuario) DO UPDATE SET
                    telefono  = excluded.telefono,
                    direccion = excluded.direccion
                """,
                (idUsuario, usuario.telefono, usuario.direccion),
            )
        elif isinstance(usuario, Tecnico):
            cursor.execute(
                """
                INSERT INTO tecnicos (idUsuario, rubroEspecialidad, disponible)
                VALUES (?, ?, ?)
                ON CONFLICT(idUsuario) DO UPDATE SET
                    rubroEspecialidad = excluded.rubroEspecialidad,
                    disponible        = excluded.disponible
                """,
                (
                    idUsuario,
                    usuario.rubroEspecialidad.value,
                    int(usuario.disponible),
                ),
            )

        self._conn.commit()
        guardado = self.obtenerPorId(idUsuario)
        if guardado is None:
            raise RuntimeError(f"No se pudo recuperar el usuario {idUsuario}.")
        return guardado

    def obtenerPorId(self, idUsuario: int) -> Usuario | None:
        row = self._conn.execute(
            _USUARIO_SELECT + " WHERE u.idUsuario = ?",
            (idUsuario,),
        ).fetchone()
        return self._row_to_usuario(row) if row is not None else None

    def listarTecnicos(self, soloDisponibles: bool = False) -> list[Tecnico]:
        sql = _USUARIO_SELECT + " WHERE u.tipo = 'TECNICO'"
        if soloDisponibles:
            sql += " AND t.disponible = 1"
        sql += " ORDER BY u.idUsuario"

        tecnicos: list[Tecnico] = []
        for row in self._conn.execute(sql).fetchall():
            usuario = self._row_to_usuario(row)
            if isinstance(usuario, Tecnico):
                tecnicos.append(usuario)
        return tecnicos

    def listarClientes(self) -> list[Cliente]:
        sql = _USUARIO_SELECT + " WHERE u.tipo = 'CLIENTE' ORDER BY u.idUsuario"
        clientes: list[Cliente] = []
        for row in self._conn.execute(sql).fetchall():
            usuario = self._row_to_usuario(row)
            if isinstance(usuario, Cliente):
                clientes.append(usuario)
        return clientes

    @staticmethod
    def _tipo_de(usuario: Usuario) -> str:
        if isinstance(usuario, Cliente):
            return "CLIENTE"
        if isinstance(usuario, Tecnico):
            return "TECNICO"
        return "USUARIO"

    @staticmethod
    def _row_to_usuario(row: sqlite3.Row) -> Usuario:
        tipo = str(row["tipo"])
        if tipo == "CLIENTE":
            return Cliente(
                idUsuario=int(row["idUsuario"]),
                nombre=str(row["nombre"]),
                email=str(row["email"]),
                telefono=str(row["telefono"] or ""),
                direccion=str(row["direccion"] or ""),
            )
        if tipo == "TECNICO":
            return Tecnico(
                idUsuario=int(row["idUsuario"]),
                nombre=str(row["nombre"]),
                email=str(row["email"]),
                rubroEspecialidad=RubroTipo(row["rubroEspecialidad"]),
                disponible=bool(row["disponible"]),
            )
        return Usuario(
            idUsuario=int(row["idUsuario"]),
            nombre=str(row["nombre"]),
            email=str(row["email"]),
        )
