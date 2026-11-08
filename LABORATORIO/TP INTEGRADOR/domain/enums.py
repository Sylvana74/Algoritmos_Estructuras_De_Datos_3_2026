from __future__ import annotations

from enum import Enum


class RubroTipo(str, Enum):
    LINEA_BLANCA = "LINEA_BLANCA"
    COCINA = "COCINA"
    ELECTRO = "ELECTRO"
    PEQUENOS_ELECTRODOMESTICOS = "PEQUENOS_ELECTRODOMESTICOS"


class EstadoTicket(str, Enum):
    ABIERTO = "ABIERTO"
    ASIGNADO = "ASIGNADO"
    CERRADO = "CERRADO"
    REABIERTO = "REABIERTO"
