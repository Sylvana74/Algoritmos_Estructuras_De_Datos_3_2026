from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime

from domain.usuario import Usuario


@dataclass(frozen=True, kw_only=True)
class Hito:
    """Hito inmutable: una vez creado no puede modificarse."""

    id: int | None = None
    mensaje: str
    fechaHora: datetime = field(default_factory=datetime.now)
    autor: Usuario

    def __post_init__(self) -> None:
        if not self.mensaje.strip():
            raise ValueError("El mensaje del hito no puede estar vacío.")
