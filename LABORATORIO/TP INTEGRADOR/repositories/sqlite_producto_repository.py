from __future__ import annotations

import sqlite3

from domain.enums import RubroTipo
from domain.producto import Producto
from repositories.interfaces import IRepositorioProducto


class SQLiteProductoRepository(IRepositorioProducto):
    def __init__(self, conn: sqlite3.Connection) -> None:
        self._conn = conn

    def guardar(self, producto: Producto) -> Producto:
        cursor = self._conn.cursor()
        if producto.idProducto is None:
            cursor.execute(
                """
                INSERT INTO productos (nombre, marca, modelo, rubro)
                VALUES (?, ?, ?, ?)
                """,
                (producto.nombre, producto.marca, producto.modelo, producto.rubro.value),
            )
            idProducto = int(cursor.lastrowid)
        else:
            cursor.execute(
                """
                UPDATE productos
                   SET nombre = ?, marca = ?, modelo = ?, rubro = ?
                 WHERE idProducto = ?
                """,
                (
                    producto.nombre,
                    producto.marca,
                    producto.modelo,
                    producto.rubro.value,
                    producto.idProducto,
                ),
            )
            idProducto = producto.idProducto

        self._conn.commit()
        return Producto(
            idProducto=idProducto,
            nombre=producto.nombre,
            marca=producto.marca,
            modelo=producto.modelo,
            rubro=producto.rubro,
        )

    def obtenerPorId(self, idProducto: int) -> Producto | None:
        row = self._conn.execute(
            """
            SELECT idProducto, nombre, marca, modelo, rubro
              FROM productos
             WHERE idProducto = ?
            """,
            (idProducto,),
        ).fetchone()
        return self._row_to_producto(row) if row is not None else None

    def listar(self) -> list[Producto]:
        rows = self._conn.execute(
            """
            SELECT idProducto, nombre, marca, modelo, rubro
              FROM productos
             ORDER BY idProducto
            """
        ).fetchall()
        return [self._row_to_producto(row) for row in rows]

    @staticmethod
    def _row_to_producto(row: sqlite3.Row) -> Producto:
        return Producto(
            idProducto=int(row["idProducto"]),
            nombre=str(row["nombre"]),
            marca=str(row["marca"]),
            modelo=str(row["modelo"]),
            rubro=RubroTipo(row["rubro"]),
        )
