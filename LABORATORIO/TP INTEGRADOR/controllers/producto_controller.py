from __future__ import annotations

from domain.enums import RubroTipo
from domain.exceptions import EntidadNoEncontradaError
from domain.producto import Producto
from repositories.interfaces import IRepositorioProducto


class ProductoController:
    def __init__(self, producto_repo: IRepositorioProducto) -> None:
        self._producto_repo = producto_repo

    def asignarTipoProducto(self, idProducto: int, rubro: RubroTipo) -> Producto:
        producto = self._producto_repo.obtenerPorId(idProducto)
        if producto is None:
            raise EntidadNoEncontradaError(
                f"No existe el producto con id {idProducto}."
            )
        producto.rubro = rubro
        return self._producto_repo.guardar(producto)

    def obtenerProducto(self, idProducto: int) -> Producto:
        producto = self._producto_repo.obtenerPorId(idProducto)
        if producto is None:
            raise EntidadNoEncontradaError(
                f"No existe el producto con id {idProducto}."
            )
        return producto
