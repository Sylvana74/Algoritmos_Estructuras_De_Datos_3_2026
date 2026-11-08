from __future__ import annotations


class TicketingError(Exception):
    """Error base del dominio de ticketing."""


class EntidadNoEncontradaError(TicketingError):
    """La entidad solicitada no existe en la persistencia."""


class TransicionEstadoInvalidaError(TicketingError):
    """El cambio de estado solicitado no está permitido."""


class SinTecnicoDisponibleError(TicketingError):
    """No hay técnicos disponibles para el rubro solicitado."""


class ReaperturaFueraDePlazoError(TicketingError):
    """La reapertura supera el plazo máximo permitido de 30 días."""
