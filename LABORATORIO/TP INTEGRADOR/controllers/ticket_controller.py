from __future__ import annotations

from datetime import datetime, timedelta

from controllers.hito_controller import HitoController
from controllers.notificacion_controller import NotificacionController
from domain.enums import EstadoTicket, RubroTipo
from domain.exceptions import (
    EntidadNoEncontradaError,
    ReaperturaFueraDePlazoError,
    SinTecnicoDisponibleError,
)
from domain.ticket import Ticket
from domain.usuario import Cliente, Usuario
from repositories.interfaces import (
    IRepositorioProducto,
    IRepositorioTicket,
    IRepositorioUsuario,
)

DIAS_MAXIMOS_REAPERTURA = 30


class TicketController:
    def __init__(
        self,
        ticket_repo: IRepositorioTicket,
        producto_repo: IRepositorioProducto,
        usuario_repo: IRepositorioUsuario,
        hito_controller: HitoController,
        notificacion_controller: NotificacionController,
    ) -> None:
        self._ticket_repo = ticket_repo
        self._producto_repo = producto_repo
        self._usuario_repo = usuario_repo
        self._hito_controller = hito_controller
        self._notificacion = notificacion_controller

    def crearTicket(
        self,
        idProducto: int,
        idCliente: int,
        mensaje: str,
        fechaCreacion: datetime | None = None,
    ) -> Ticket:
        producto = self._producto_repo.obtenerPorId(idProducto)
        if producto is None:
            raise EntidadNoEncontradaError(
                f"No existe el producto con id {idProducto}."
            )

        cliente = self._usuario_repo.obtenerPorId(idCliente)
        if not isinstance(cliente, Cliente):
            raise EntidadNoEncontradaError(
                f"No existe el cliente con id {idCliente}."
            )

        rubro = producto.obtenerRubro()
        ticket = Ticket(
            fechaCreacion=fechaCreacion or datetime.now(),
            estado=EstadoTicket.ABIERTO,
            descripcion=mensaje,
            producto=producto,
            cliente=cliente,
        )
        ticket.crearTicket(mensaje)

        guardado = self._ticket_repo.guardar(ticket)
        self._hito_controller.agregarHito(
            guardado,
            (
                f"Ticket creado. Producto: {producto.nombre} {producto.marca} "
                f"{producto.modelo}. Rubro: {rubro.value}."
            ),
            cliente,
        )
        return guardado

    def iniciarAsignacion(self, idTicket: int, rubroTicket: RubroTipo) -> Ticket:
        ticket = self._obtenerTicket(idTicket)

        candidatos = [
            tecnico
            for tecnico in self._usuario_repo.listarTecnicos(soloDisponibles=True)
            if tecnico.puedeAtender(rubroTicket)
        ]
        if not candidatos:
            raise SinTecnicoDisponibleError(
                f"No hay técnicos disponibles para el rubro {rubroTicket.value}."
            )

        tecnico = candidatos[0]
        tecnicoAnterior = ticket.tecnico
        ticket.tecnico = tecnico
        ticket.cambiarEstado(EstadoTicket.ASIGNADO)

        if (
            tecnicoAnterior is not None
            and tecnicoAnterior.idUsuario != tecnico.idUsuario
        ):
            tecnicoAnterior.disponible = True
            self._usuario_repo.guardar(tecnicoAnterior)

        tecnico.disponible = False
        self._usuario_repo.guardar(tecnico)
        guardado = self._ticket_repo.guardar(ticket)

        self._notificacion.notificarCliente(
            guardado.cliente,
            (
                f"Su ticket #{guardado.idTicket} fue asignado al técnico "
                f"{tecnico.nombre} ({tecnico.rubroEspecialidad.value})."
            ),
        )
        self._notificacion.notificarTecnico(
            tecnico,
            f"Se le asignó el ticket #{guardado.idTicket}: {guardado.descripcion}",
        )
        return guardado

    def cambiarEstado(self, idTicket: int, nuevoEstado: EstadoTicket) -> Ticket:
        ticket = self._obtenerTicket(idTicket)
        ticket.cambiarEstado(nuevoEstado)
        return self._ticket_repo.guardar(ticket)

    def cerrarTicket(self, idTicket: int, autor: Usuario) -> Ticket:
        ticket = self._obtenerTicket(idTicket)
        ticket.cambiarEstado(EstadoTicket.CERRADO)
        ticket.fechaCierre = datetime.now()

        if ticket.tecnico is not None:
            ticket.tecnico.disponible = True
            self._usuario_repo.guardar(ticket.tecnico)

        guardado = self._ticket_repo.guardar(ticket)
        self._hito_controller.agregarHito(
            guardado,
            f"Ticket cerrado por {autor.nombre}.",
            autor,
        )
        self._notificacion.notificarCierre(guardado)
        return guardado

    def reabrirTicket(
        self,
        idTicket: int,
        autor: Usuario,
        fechaReferencia: datetime | None = None,
    ) -> Ticket:
        ticket = self._obtenerTicket(idTicket)
        if ticket.estado != EstadoTicket.CERRADO:
            raise ValueError("Solo se pueden reabrir tickets en estado CERRADO.")
        if ticket.fechaCierre is None:
            raise ValueError("El ticket no registra fecha de cierre.")

        ahora = fechaReferencia or datetime.now()
        if ahora - ticket.fechaCierre > timedelta(days=DIAS_MAXIMOS_REAPERTURA):
            raise ReaperturaFueraDePlazoError(
                "No se puede reabrir: transcurrieron más de "
                f"{DIAS_MAXIMOS_REAPERTURA} días desde el cierre."
            )

        ticket.cambiarEstado(EstadoTicket.REABIERTO)
        ticket.fechaCierre = None
        guardado = self._ticket_repo.guardar(ticket)
        self._hito_controller.agregarHito(
            guardado,
            f"Ticket reabierto por {autor.nombre}.",
            autor,
        )

        candidatos = [
            tecnico
            for tecnico in self._usuario_repo.listarTecnicos(soloDisponibles=True)
            if tecnico.puedeAtender(ticket.producto.obtenerRubro())
        ]
        if candidatos:
            tecnico = candidatos[0]
            guardado.tecnico = tecnico
            tecnico.disponible = False
            self._usuario_repo.guardar(tecnico)
            guardado = self._ticket_repo.guardar(guardado)

            self._notificacion.notificarCliente(
                guardado.cliente,
                (
                    f"El ticket #{guardado.idTicket} fue reasignado al técnico "
                    f"{tecnico.nombre}."
                ),
            )
            self._notificacion.notificarTecnico(
                tecnico,
                f"El ticket #{guardado.idTicket} fue reabierto y asignado a usted.",
            )

        self._notificacion.notificarReapertura(guardado)
        return guardado

    def _obtenerTicket(self, idTicket: int) -> Ticket:
        ticket = self._ticket_repo.obtenerTicket(idTicket)
        if ticket is None:
            raise EntidadNoEncontradaError(
                f"No existe el ticket con id {idTicket}."
            )
        return ticket
