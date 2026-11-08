from __future__ import annotations

import sqlite3
from datetime import datetime

from domain.hito import Hito
from repositories.interfaces import IRepositorioHito, IRepositorioUsuario


class SQLiteHitoRepository(IRepositorioHito):
    def __init__(
        self,
        conn: sqlite3.Connection,
        usuario_repo: IRepositorioUsuario,
    ) -> None:
        self._conn = conn
        self._usuario_repo = usuario_repo

    def crear(self, hito: Hito, idTicket: int) -> Hito:
        if hito.autor.idUsuario is None:
            raise ValueError("El autor del hito debe estar persistido.")

        cursor = self._conn.execute(
            """
            INSERT INTO hitos (mensaje, fechaHora, idAutor, idTicket)
            VALUES (?, ?, ?, ?)
            """,
            (
                hito.mensaje,
                hito.fechaHora.isoformat(),
                hito.autor.idUsuario,
                idTicket,
            ),
        )
        self._conn.commit()

        return Hito(
            id=int(cursor.lastrowid),
            mensaje=hito.mensaje,
            fechaHora=hito.fechaHora,
            autor=hito.autor,
        )

    def listarPorTicket(self, idTicket: int) -> list[Hito]:
        rows = self._conn.execute(
            """
            SELECT idHito, mensaje, fechaHora, idAutor
              FROM hitos
             WHERE idTicket = ?
             ORDER BY fechaHora, idHito
            """,
            (idTicket,),
        ).fetchall()

        hitos: list[Hito] = []
        for row in rows:
            autor = self._usuario_repo.obtenerPorId(int(row["idAutor"]))
            if autor is None:
                continue
            hitos.append(
                Hito(
                    id=int(row["idHito"]),
                    mensaje=str(row["mensaje"]),
                    fechaHora=datetime.fromisoformat(str(row["fechaHora"])),
                    autor=autor,
                )
            )
        return hitos
