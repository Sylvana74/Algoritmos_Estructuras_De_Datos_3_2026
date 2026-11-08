from __future__ import annotations

import sqlite3
from datetime import datetime

from domain.enums import EstadoTicket
from domain.ticket import Ticket
from domain.usuario import Cliente, Tecnico
from repositories.interfaces import (
    IRepositorioHito,
    IRepositorioProducto,
    IRepositorioTicket,
    IRepositorioUsuario,
)


class SQLiteTicketRepository(IRepositorioTicket):
    def __init__(
        self,
        conn: sqlite3.Connection,
        producto_repo: IRepositorioProducto,
        usuario_repo: IRepositorioUsuario,
        hito_repo: IRepositorioHito,
    ) -> None:
        self._conn = conn
        self._producto_repo = producto_repo
        self._usuario_repo = usuario_repo
        self._hito_repo = hito_repo

    def guardar(self, ticket: Ticket) -> Ticket:
        if ticket.producto.idProducto is None:
            raise ValueError("El producto del ticket debe estar persistido.")
        if ticket.cliente.idUsuario is None:
            raise ValueError("El cliente del ticket debe estar persistido.")

        cursor = self._conn.cursor()
        fechaCreacion = ticket.fechaCreacion.isoformat()
        fechaCierre = ticket.fechaCierre.isoformat() if ticket.fechaCierre else None
        idTecnico = ticket.tecnico.idUsuario if ticket.tecnico else None

        if ticket.idTicket is None:
            cursor.execute(
                """
                INSERT INTO tickets (
                    fechaCreacion, estado, descripcion,
                    idProducto, idCliente, idTecnico, fechaCierre
                )
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    fechaCreacion,
                    ticket.estado.value,
                    ticket.descripcion,
                    ticket.producto.idProducto,
                    ticket.cliente.idUsuario,
                    idTecnico,
                    fechaCierre,
                ),
            )
            idTicket = int(cursor.lastrowid)
        else:
            cursor.execute(
                """
                UPDATE tickets
                   SET fechaCreacion = ?,
                       estado        = ?,
                       descripcion   = ?,
                       idProducto    = ?,
                       idCliente     = ?,
                       idTecnico     = ?,
                       fechaCierre   = ?
                 WHERE idTicket = ?
                """,
                (
                    fechaCreacion,
                    ticket.estado.value,
                    ticket.descripcion,
                    ticket.producto.idProducto,
                    ticket.cliente.idUsuario,
                    idTecnico,
                    fechaCierre,
                    ticket.idTicket,
                ),
            )
            idTicket = ticket.idTicket

        self._conn.commit()
        return Ticket(
            idTicket=idTicket,
            fechaCreacion=ticket.fechaCreacion,
            estado=ticket.estado,
            descripcion=ticket.descripcion,
            producto=ticket.producto,
            cliente=ticket.cliente,
            tecnico=ticket.tecnico,
            hitos=list(ticket.hitos),
            fechaCierre=ticket.fechaCierre,
        )

    def obtenerTicket(self, idTicket: int) -> Ticket | None:
        row = self._conn.execute(
            """
            SELECT idTicket, fechaCreacion, estado, descripcion,
                   idProducto, idCliente, idTecnico, fechaCierre
              FROM tickets
             WHERE idTicket = ?
            """,
            (idTicket,),
        ).fetchone()
        return self._row_to_ticket(row) if row is not None else None

    def listarPorCliente(self, idUsuario: int) -> list[Ticket]:
        return self._listar(
            "SELECT idTicket FROM tickets WHERE idCliente = ? ORDER BY idTicket",
            (idUsuario,),
        )

    def listarPorTecnico(self, idUsuario: int) -> list[Ticket]:
        return self._listar(
            "SELECT idTicket FROM tickets WHERE idTecnico = ? ORDER BY idTicket",
            (idUsuario,),
        )

    def listarTodos(self) -> list[Ticket]:
        return self._listar("SELECT idTicket FROM tickets ORDER BY idTicket", ())

    def _listar(
        self,
        sql: str,
        parametros: tuple[object, ...],
    ) -> list[Ticket]:
        tickets: list[Ticket] = []
        for row in self._conn.execute(sql, parametros).fetchall():
            ticket = self.obtenerTicket(int(row["idTicket"]))
            if ticket is not None:
                tickets.append(ticket)
        return tickets

    def _row_to_ticket(self, row: sqlite3.Row) -> Ticket:
        producto = self._producto_repo.obtenerPorId(int(row["idProducto"]))
        cliente = self._usuario_repo.obtenerPorId(int(row["idCliente"]))
        if producto is None or not isinstance(cliente, Cliente):
            raise RuntimeError(
                f"Ticket {row['idTicket']} con producto o cliente inválido."
            )

        tecnico: Tecnico | None = None
        if row["idTecnico"] is not None:
            usuarioTecnico = self._usuario_repo.obtenerPorId(int(row["idTecnico"]))
            if isinstance(usuarioTecnico, Tecnico):
                tecnico = usuarioTecnico

        fechaCierre = (
            datetime.fromisoformat(str(row["fechaCierre"]))
            if row["fechaCierre"] is not None
            else None
        )

        return Ticket(
            idTicket=int(row["idTicket"]),
            fechaCreacion=datetime.fromisoformat(str(row["fechaCreacion"])),
            estado=EstadoTicket(row["estado"]),
            descripcion=str(row["descripcion"]),
            producto=producto,
            cliente=cliente,
            tecnico=tecnico,
            hitos=self._hito_repo.listarPorTicket(int(row["idTicket"])),
            fechaCierre=fechaCierre,
        )
