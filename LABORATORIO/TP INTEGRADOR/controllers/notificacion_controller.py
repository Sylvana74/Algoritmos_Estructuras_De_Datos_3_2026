from __future__ import annotations

from domain.ticket import Ticket
from domain.usuario import Cliente, Tecnico


class NotificacionController:
    """Canal de notificaciones. En esta demo se emiten por consola."""

    def __init__(self) -> None:
        self._historial: list[str] = []

    def notificarCliente(self, cliente: Cliente, mensaje: str) -> None:
        self._emitir(f"Cliente {cliente.nombre} <{cliente.email}>", mensaje)

    def notificarTecnico(self, tecnico: Tecnico, mensaje: str) -> None:
        self._emitir(f"Técnico {tecnico.nombre} <{tecnico.email}>", mensaje)

    def notificarCierre(self, ticket: Ticket) -> None:
        self._emitir(
            f"Cliente {ticket.cliente.nombre} <{ticket.cliente.email}>",
            f"El ticket #{ticket.idTicket} fue CERRADO.",
        )
        if ticket.tecnico is not None:
            self.notificarTecnico(
                ticket.tecnico,
                f"El ticket #{ticket.idTicket} fue cerrado por el cliente.",
            )

    def notificarReapertura(self, ticket: Ticket) -> None:
        self._emitir(
            f"Cliente {ticket.cliente.nombre} <{ticket.cliente.email}>",
            f"El ticket #{ticket.idTicket} fue REABIERTO correctamente.",
        )
        if ticket.tecnico is not None:
            self.notificarTecnico(
                ticket.tecnico,
                f"El ticket #{ticket.idTicket} fue reabierto y requiere atención.",
            )

    @property
    def historial(self) -> list[str]:
        return list(self._historial)

    def _emitir(self, destino: str, mensaje: str) -> None:
        texto = f"[NOTIFICACIÓN -> {destino}] {mensaje}"
        self._historial.append(texto)
        print(texto)
