from __future__ import annotations

from dataclasses import dataclass

from domain.enums import RubroTipo


@dataclass(kw_only=True)
class Usuario:
    nombre: str
    email: str
    idUsuario: int | None = None

    def __post_init__(self) -> None:
        if not self.nombre.strip():
            raise ValueError("El nombre del usuario no puede estar vacío.")
        if "@" not in self.email:
            raise ValueError(f"Email inválido: {self.email!r}")


@dataclass(kw_only=True)
class Cliente(Usuario):
    telefono: str = ""
    direccion: str = ""

    def solicitarCierreTicket(self) -> str:
        return f"El cliente {self.nombre} solicita el cierre del ticket."

    def solicitarReaperturaTicket(self) -> str:
        return f"El cliente {self.nombre} solicita la reapertura del ticket."


@dataclass(kw_only=True)
class Tecnico(Usuario):
    rubroEspecialidad: RubroTipo = RubroTipo.LINEA_BLANCA
    disponible: bool = True

    def puedeAtender(self, rubro: RubroTipo) -> bool:
        return self.rubroEspecialidad == rubro
