from __future__ import annotations

from abc import ABC, abstractmethod

from domain.hito import Hito
from domain.producto import Producto
from domain.ticket import Ticket
from domain.usuario import Cliente, Tecnico, Usuario


class IRepositorioProducto(ABC):
    @abstractmethod
    def guardar(self, producto: Producto) -> Producto:
        ...

    @abstractmethod
    def obtenerPorId(self, idProducto: int) -> Producto | None:
        ...


class IRepositorioTicket(ABC):
    @abstractmethod
    def guardar(self, ticket: Ticket) -> Ticket:
        ...

    @abstractmethod
    def obtenerTicket(self, idTicket: int) -> Ticket | None:
        ...

    @abstractmethod
    def listarPorCliente(self, idUsuario: int) -> list[Ticket]:
        ...

    @abstractmethod
    def listarPorTecnico(self, idUsuario: int) -> list[Ticket]:
        ...


class IRepositorioHito(ABC):
    @abstractmethod
    def crear(self, hito: Hito, idTicket: int) -> Hito:
        ...

    @abstractmethod
    def listarPorTicket(self, idTicket: int) -> list[Hito]:
        ...


class IRepositorioUsuario(ABC):
    """Repositorio auxiliar para resolver la asignación de técnicos y clientes."""

    @abstractmethod
    def guardar(self, usuario: Usuario) -> Usuario:
        ...

    @abstractmethod
    def obtenerPorId(self, idUsuario: int) -> Usuario | None:
        ...

    @abstractmethod
    def listarTecnicos(self, soloDisponibles: bool = False) -> list[Tecnico]:
        ...

    @abstractmethod
    def listarClientes(self) -> list[Cliente]:
        ...
