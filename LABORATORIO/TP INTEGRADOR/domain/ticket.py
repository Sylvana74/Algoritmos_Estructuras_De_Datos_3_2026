from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime

from domain.enums import EstadoTicket
from domain.exceptions import TransicionEstadoInvalidaError
from domain.hito import Hito
from domain.producto import Producto
from domain.usuario import Cliente, Tecnico

_TRANSICIONES_PERMITIDAS: dict[EstadoTicket, set[EstadoTicket]] = {
    EstadoTicket.ABIERTO: {EstadoTicket.ASIGNADO, EstadoTicket.CERRADO},
    EstadoTicket.ASIGNADO: {EstadoTicket.ABIERTO, EstadoTicket.CERRADO},
    EstadoTicket.CERRADO: {EstadoTicket.REABIERTO},
    EstadoTicket.REABIERTO: {EstadoTicket.ASIGNADO, EstadoTicket.CERRADO},
}


@dataclass(kw_only=True)
class Ticket:
    idTicket: int | None = None
    fechaCreacion: datetime = field(default_factory=datetime.now)
    estado: EstadoTicket = EstadoTicket.ABIERTO
    descripcion: str
    producto: Producto
    cliente: Cliente
    tecnico: Tecnico | None = None
    hitos: list[Hito] = field(default_factory=list)
    fechaCierre: datetime | None = None

    def crearTicket(self, mensaje: str) -> "Ticket":
        self.descripcion = mensaje
        self.estado = EstadoTicket.ABIERTO
        return self

    def cambiarEstado(self, nuevoEstado: EstadoTicket) -> None:
        if nuevoEstado == self.estado:
            return
        permitidos = _TRANSICIONES_PERMITIDAS.get(self.estado, set())
        if nuevoEstado not in permitidos:
            raise TransicionEstadoInvalidaError(
                f"No se puede pasar de {self.estado.value} a {nuevoEstado.value}."
            )
        self.estado = nuevoEstado
