"""
Modelo de datos para tags de elementos de área

Este módulo define el modelo AreaElementTag que representa
los tags que pueden asignarse a elementos dentro de áreas.
"""

from dataclasses import dataclass, asdict
from datetime import datetime
from typing import Optional, Dict, Any


@dataclass
class AreaElementTag:
    """
    Modelo para tags de elementos de área

    Los tags permiten categorizar y filtrar elementos dentro de áreas
    (items, categorías, listas, tablas, procesos, etc.)

    Attributes:
        id: Identificador único del tag
        name: Nombre del tag (único)
        color: Color en formato hex (ej: #9b59b6)
        description: Descripción opcional del tag
        created_at: Fecha de creación
        updated_at: Fecha de última actualización
    """
    id: int
    name: str
    color: str = '#9b59b6'
    description: str = ''
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    def to_dict(self) -> Dict[str, Any]:
        """
        Convierte el tag a diccionario

        Returns:
            Diccionario con todos los campos del tag
        """
        data = asdict(self)

        # Convertir datetime a string ISO
        if self.created_at:
            data['created_at'] = self.created_at.isoformat()
        if self.updated_at:
            data['updated_at'] = self.updated_at.isoformat()

        return data

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'AreaElementTag':
        """
        Crea un tag desde un diccionario

        Args:
            data: Diccionario con datos del tag

        Returns:
            Instancia de AreaElementTag
        """
        # Convertir strings ISO a datetime
        if 'created_at' in data and isinstance(data['created_at'], str):
            data['created_at'] = datetime.fromisoformat(data['created_at'])
        if 'updated_at' in data and isinstance(data['updated_at'], str):
            data['updated_at'] = datetime.fromisoformat(data['updated_at'])

        return cls(**data)

    def __str__(self) -> str:
        """Representación en string del tag"""
        return f"Tag({self.name})"

    def __repr__(self) -> str:
        """Representación detallada del tag"""
        return f"AreaElementTag(id={self.id}, name='{self.name}', color='{self.color}')"

    def __eq__(self, other) -> bool:
        """Compara dos tags por ID"""
        if not isinstance(other, AreaElementTag):
            return False
        return self.id == other.id

    def __hash__(self) -> int:
        """Hash basado en el ID para usar en sets/dicts"""
        return hash(self.id)


# Funciones auxiliares para trabajar con tags

def create_tag_from_db_row(row: Dict[str, Any]) -> AreaElementTag:
    """
    Crea un AreaElementTag desde una fila de base de datos

    Args:
        row: Diccionario con datos de la BD (puede tener campos extra)

    Returns:
        Instancia de AreaElementTag
    """
    # Filtrar solo los campos relevantes
    tag_data = {
        'id': row['id'],
        'name': row['name'],
        'color': row.get('color', '#9b59b6'),
        'description': row.get('description', ''),
        'created_at': row.get('created_at'),
        'updated_at': row.get('updated_at'),
    }

    return AreaElementTag.from_dict(tag_data)


def tags_to_dict_list(tags: list) -> list:
    """
    Convierte una lista de tags a lista de diccionarios

    Args:
        tags: Lista de AreaElementTag

    Returns:
        Lista de diccionarios
    """
    return [tag.to_dict() for tag in tags]


def tags_from_dict_list(data: list) -> list:
    """
    Convierte una lista de diccionarios a lista de tags

    Args:
        data: Lista de diccionarios

    Returns:
        Lista de AreaElementTag
    """
    return [AreaElementTag.from_dict(item) for item in data]


def get_tag_ids(tags: list) -> list:
    """
    Extrae los IDs de una lista de tags

    Args:
        tags: Lista de AreaElementTag

    Returns:
        Lista de IDs (int)
    """
    return [tag.id for tag in tags]


def filter_tags_by_name(tags: list, query: str) -> list:
    """
    Filtra tags por coincidencia parcial en el nombre

    Args:
        tags: Lista de AreaElementTag
        query: Texto a buscar (case-insensitive)

    Returns:
        Lista de tags filtrados
    """
    query_lower = query.lower()
    return [tag for tag in tags if query_lower in tag.name.lower()]


def sort_tags_by_name(tags: list, reverse: bool = False) -> list:
    """
    Ordena tags alfabéticamente por nombre

    Args:
        tags: Lista de AreaElementTag
        reverse: Si True, ordena en orden descendente

    Returns:
        Lista de tags ordenados
    """
    return sorted(tags, key=lambda t: t.name.lower(), reverse=reverse)
