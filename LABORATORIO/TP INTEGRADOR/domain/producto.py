from __future__ import annotations

from dataclasses import dataclass

from domain.enums import RubroTipo


@dataclass(kw_only=True)
class Producto:
    idProducto: int | None = None
    nombre: str
    marca: str
    modelo: str
    rubro: RubroTipo

    def obtenerRubro(self) -> RubroTipo:
        return self.rubro
