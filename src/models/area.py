"""
Modelos de datos para el sistema de áreas

Modelos:
- Area: Área principal
- AreaRelation: Relación entre área y entidad (tag, lista, item, etc)
- AreaComponent: Componente estructural (divisor, comentario, alerta, nota)
"""

from dataclasses import dataclass, field, asdict
from datetime import datetime
from typing import Optional, Dict, Any, List, TYPE_CHECKING

# Evitar import circular usando TYPE_CHECKING
if TYPE_CHECKING:
    from .area_element_tag import AreaElementTag


@dataclass
class Area:
    """
    Modelo de área

    Un área agrupa tags, procesos, listas, tablas, categorías e items relacionados
    para facilitar el acceso rápido a todos los elementos de un área específica
    (por ejemplo: Frontend, Backend, DevOps, Database, etc).
    """
    id: int
    name: str
    description: str = ""
    color: str = "#9b59b6"
    icon: str = "🏢"
    is_active: bool = True
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convierte el área a diccionario"""
        data = asdict(self)
        # Convertir datetime a string ISO
        if self.created_at:
            data['created_at'] = self.created_at.isoformat()
        if self.updated_at:
            data['updated_at'] = self.updated_at.isoformat()
        return data

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Area':
        """Crea un área desde un diccionario"""
        # Convertir strings ISO a datetime
        if 'created_at' in data and isinstance(data['created_at'], str):
            data['created_at'] = datetime.fromisoformat(data['created_at'])
        if 'updated_at' in data and isinstance(data['updated_at'], str):
            data['updated_at'] = datetime.fromisoformat(data['updated_at'])
        return cls(**data)

    def __str__(self) -> str:
        return f"{self.icon} {self.name}"


@dataclass
class AreaRelation:
    """
    Modelo de relación área-entidad

    Representa la asociación entre un área y una entidad
    (tag, proceso, lista, tabla, categoría o item).

    Attributes:
        id: Identificador único de la relación
        area_id: ID del área al que pertenece
        entity_type: Tipo de entidad relacionada
        entity_id: ID de la entidad relacionada
        description: Descripción contextual del elemento
        order_index: Orden de visualización en el área
        created_at: Fecha de creación
        tags: Lista de tags asociados a esta relación
    """
    id: int
    area_id: int
    entity_type: str  # 'tag', 'process', 'list', 'table', 'category', 'item'
    entity_id: int
    description: str = ""  # Descripción contextual del elemento en el área
    order_index: int = 0
    created_at: Optional[datetime] = None
    tags: List['AreaElementTag'] = field(default_factory=list)

    # Tipos de entidad válidos
    VALID_ENTITY_TYPES = {'tag', 'process', 'list', 'table', 'category', 'item'}

    def __post_init__(self):
        """Validación post-inicialización"""
        if self.entity_type not in self.VALID_ENTITY_TYPES:
            raise ValueError(
                f"entity_type inválido: '{self.entity_type}'. "
                f"Debe ser uno de: {', '.join(self.VALID_ENTITY_TYPES)}"
            )

    def to_dict(self, include_tags: bool = True) -> Dict[str, Any]:
        """
        Convierte la relación a diccionario

        Args:
            include_tags: Si True, incluye la lista de tags en el diccionario

        Returns:
            Diccionario con datos de la relación
        """
        data = asdict(self)

        # Convertir datetime
        if self.created_at:
            data['created_at'] = self.created_at.isoformat()

        # Convertir tags a lista de diccionarios
        if include_tags and self.tags:
            data['tags'] = [tag.to_dict() for tag in self.tags]
        elif not include_tags:
            data.pop('tags', None)

        return data

    @classmethod
    def from_dict(cls, data: Dict[str, Any], include_tags: bool = True) -> 'AreaRelation':
        """
        Crea una relación desde un diccionario

        Args:
            data: Diccionario con datos de la relación
            include_tags: Si True, carga los tags desde el diccionario

        Returns:
            Instancia de AreaRelation
        """
        # Convertir strings ISO a datetime
        if 'created_at' in data and isinstance(data['created_at'], str):
            data['created_at'] = datetime.fromisoformat(data['created_at'])

        # Convertir lista de tags si existe
        if include_tags and 'tags' in data and data['tags']:
            from .area_element_tag import AreaElementTag
            data['tags'] = [AreaElementTag.from_dict(tag_data) for tag_data in data['tags']]
        else:
            data.pop('tags', None)

        return cls(**data)

    def add_tag(self, tag: 'AreaElementTag') -> None:
        """
        Agrega un tag a esta relación

        Args:
            tag: Tag a agregar
        """
        if tag not in self.tags:
            self.tags.append(tag)

    def remove_tag(self, tag: 'AreaElementTag') -> None:
        """
        Remueve un tag de esta relación

        Args:
            tag: Tag a remover
        """
        if tag in self.tags:
            self.tags.remove(tag)

    def remove_tag_by_id(self, tag_id: int) -> None:
        """
        Remueve un tag por su ID

        Args:
            tag_id: ID del tag a remover
        """
        self.tags = [tag for tag in self.tags if tag.id != tag_id]

    def has_tag(self, tag: 'AreaElementTag') -> bool:
        """
        Verifica si esta relación tiene un tag específico

        Args:
            tag: Tag a verificar

        Returns:
            True si el tag está asociado
        """
        return tag in self.tags

    def has_tag_by_id(self, tag_id: int) -> bool:
        """
        Verifica si esta relación tiene un tag por ID

        Args:
            tag_id: ID del tag a verificar

        Returns:
            True si el tag está asociado
        """
        return any(tag.id == tag_id for tag in self.tags)

    def get_tag_ids(self) -> List[int]:
        """
        Obtiene los IDs de todos los tags asociados

        Returns:
            Lista de IDs de tags
        """
        return [tag.id for tag in self.tags]

    def __str__(self) -> str:
        tag_count = len(self.tags)
        return f"AreaRelation({self.entity_type}#{self.entity_id} -> Area#{self.area_id}, {tag_count} tags)"


@dataclass
class AreaComponent:
    """
    Modelo de componente estructural del área

    Componentes que ayudan a organizar visualmente el área:
    - divider: Línea divisoria horizontal
    - comment: Comentario/documentación
    - alert: Alerta importante
    - note: Nota/recordatorio
    """
    id: int
    area_id: int
    component_type: str  # 'divider', 'comment', 'alert', 'note'
    content: str = ""  # Texto del componente (vacío para divisores)
    order_index: int = 0
    created_at: Optional[datetime] = None

    # Tipos de componente válidos
    VALID_COMPONENT_TYPES = {'divider', 'comment', 'alert', 'note'}

    # Íconos por tipo de componente
    COMPONENT_ICONS = {
        'divider': '─',
        'comment': '💬',
        'alert': '⚠️',
        'note': '📌'
    }

    def __post_init__(self):
        """Validación post-inicialización"""
        if self.component_type not in self.VALID_COMPONENT_TYPES:
            raise ValueError(
                f"component_type inválido: '{self.component_type}'. "
                f"Debe ser uno de: {', '.join(self.VALID_COMPONENT_TYPES)}"
            )

    def to_dict(self) -> Dict[str, Any]:
        """Convierte el componente a diccionario"""
        data = asdict(self)
        if self.created_at:
            data['created_at'] = self.created_at.isoformat()
        return data

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'AreaComponent':
        """Crea un componente desde un diccionario"""
        if 'created_at' in data and isinstance(data['created_at'], str):
            data['created_at'] = datetime.fromisoformat(data['created_at'])
        return cls(**data)

    def get_icon(self) -> str:
        """Retorna el ícono del componente"""
        return self.COMPONENT_ICONS.get(self.component_type, '')

    def get_display_text(self) -> str:
        """Retorna el texto a mostrar del componente"""
        if self.component_type == 'divider':
            return '─' * 50  # Línea divisoria
        else:
            icon = self.get_icon()
            return f"{icon} {self.content}"

    def __str__(self) -> str:
        return f"{self.get_icon()} {self.component_type}: {self.content[:30]}..."


# Función auxiliar para validar tipos de entidad
def validate_entity_type(entity_type: str) -> bool:
    """Valida si el tipo de entidad es válido"""
    return entity_type in AreaRelation.VALID_ENTITY_TYPES


# Función auxiliar para validar tipos de componente
def validate_component_type(component_type: str) -> bool:
    """Valida si el tipo de componente es válido"""
    return component_type in AreaComponent.VALID_COMPONENT_TYPES


# Funciones auxiliares para obtener metadata de entidades
def get_entity_type_icon(entity_type: str) -> str:
    """Retorna el ícono correspondiente al tipo de entidad"""
    icons = {
        'tag': '🏷️',
        'process': '🔄',
        'list': '📋',
        'table': '📊',
        'category': '📁',
        'item': '📝'
    }
    return icons.get(entity_type, '📄')


def get_entity_type_label(entity_type: str) -> str:
    """Retorna la etiqueta legible del tipo de entidad"""
    labels = {
        'tag': 'Tag',
        'process': 'Proceso',
        'list': 'Lista',
        'table': 'Tabla',
        'category': 'Categoría',
        'item': 'Item'
    }
    return labels.get(entity_type, entity_type.title())
