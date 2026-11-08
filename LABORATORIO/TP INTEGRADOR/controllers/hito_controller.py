from __future__ import annotations

from datetime import datetime

from controllers.notificacion_controller import NotificacionController
from domain.hito import Hito
from domain.ticket import Ticket
from domain.usuario import Cliente, Tecnico, Usuario
from repositories.interfaces import IRepositorioHito


class HitoController:
    def __init__(
        self,
        hito_repo: IRepositorioHito,
        notificacion_controller: NotificacionController,
    ) -> None:
        self._hito_repo = hito_repo
        self._notificacion = notificacion_controller

    def agregarHito(self, ticket: Ticket, mensaje: str, autor: Usuario) -> Hito:
        if ticket.idTicket is None:
            raise ValueError("El ticket debe estar persistido antes de agregar hitos.")

        hito = Hito(
            mensaje=mensaje,
            fechaHora=datetime.now(),
            autor=autor,
        )
        hito_persistido = self._hito_repo.crear(hito, ticket.idTicket)
        ticket.hitos.append(hito_persistido)
        self._notificar_contraparte(ticket, autor, mensaje)
        return hito_persistido

    def _notificar_contraparte(
        self,
        ticket: Ticket,
        autor: Usuario,
        mensaje: str,
    ) -> None:
        if isinstance(autor, Tecnico):
            self._notificacion.notificarCliente(
                ticket.cliente,
                f"Nuevo mensaje del técnico {autor.nombre}: {mensaje}",
            )
        elif isinstance(autor, Cliente) and ticket.tecnico is not None:
            self._notificacion.notificarTecnico(
                ticket.tecnico,
                f"Nuevo mensaje del cliente {autor.nombre}: {mensaje}",
            )
