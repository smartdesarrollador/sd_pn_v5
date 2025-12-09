# -*- coding: utf-8 -*-
"""
Category Tag Model - Modelo de datos para tags de categorías

Representa un tag que puede ser asignado a categorías para su organización.
"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class CategoryTag:
    """
    Modelo de datos para un tag de categoría

    Attributes:
        id: ID único del tag
        name: Nombre del tag (normalizado a minúsculas)
        color: Color del tag para visualización (hex)
        created_at: Timestamp de creación
        updated_at: Timestamp de última actualización
    """

    id: int
    name: str
    color: str = "#3498db"  # Azul por defecto
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

    def __post_init__(self):
        """Normalizar nombre del tag a minúsculas"""
        if self.name:
            self.name = self.name.strip().lower()
