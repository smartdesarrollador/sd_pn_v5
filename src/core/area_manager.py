"""
Area Manager - Gestión de lógica de negocio de áreas

Responsabilidades:
- Gestión de áreas con caché
- Validaciones de negocio
- Emisión de señales PyQt6
- Métodos de utilidad
"""

import logging
from typing import List, Dict, Optional, Tuple, Any
from PyQt6.QtCore import QObject, pyqtSignal

from src.database.db_manager import DBManager
from src.models.area import Area, AreaRelation, AreaComponent, validate_entity_type

logger = logging.getLogger(__name__)


class AreaManager(QObject):
    """
    Manager para gestión de áreas

    Maneja lógica de negocio, caché y señales para el sistema de áreas
    """

    # Señales
    area_created = pyqtSignal(dict)  # area_data
    area_updated = pyqtSignal(dict)  # area_data
    area_deleted = pyqtSignal(int)   # area_id
    relation_added = pyqtSignal(int, str, int)  # area_id, entity_type, entity_id
    relation_removed = pyqtSignal(int, str, int)
    component_added = pyqtSignal(int, str)  # area_id, component_type
    component_removed = pyqtSignal(int)  # component_id

    def __init__(self, db_manager: DBManager):
        super().__init__()
        self.db = db_manager
        self._areas_cache: Dict[int, Dict] = {}
        self._cache_enabled = True
        logger.info("AreaManager initialized")

    # ==================== CACHE ====================

    def invalidate_cache(self):
        """Invalida el caché de áreas"""
        self._areas_cache.clear()
        logger.debug("Areas cache invalidated")

    def _cache_area(self, area: Dict):
        """Agrega un área al caché"""
        if self._cache_enabled and area:
            self._areas_cache[area['id']] = area

    def _get_from_cache(self, area_id: int) -> Optional[Dict]:
        """Obtiene un área del caché"""
        if self._cache_enabled:
            return self._areas_cache.get(area_id)
        return None

    # ==================== CRUD ÁREAS ====================

    def create_area(self, name: str, description: str = "",
                      color: str = "#9b59b6", icon: str = "🏢") -> Optional[Dict]:
        """
        Crea una nueva área con validación

        Args:
            name: Nombre del área
            description: Descripción
            color: Color en formato hex
            icon: Emoji icono

        Returns:
            Diccionario con datos del área creada o None si falla
        """
        # Validar nombre
        is_valid, error_msg = self.validate_area_name(name)
        if not is_valid:
            logger.error(f"Validación fallida: {error_msg}")
            return None

        try:
            area_id = self.db.add_area(name, description, color, icon)
            area = self.db.get_area(area_id)

            if area:
                self._cache_area(area)
                self.area_created.emit(area)
                logger.info(f"Área creada: {name} (ID: {area_id})")

            return area

        except Exception as e:
            logger.error(f"Error creando área: {e}")
            return None

    def get_area(self, area_id: int) -> Optional[Dict]:
        """Obtiene un área (usa caché)"""
        # Intentar desde caché
        cached = self._get_from_cache(area_id)
        if cached:
            return cached

        # Obtener de BD
        area = self.db.get_area(area_id)
        if area:
            self._cache_area(area)

        return area

    def get_all_areas(self, active_only: bool = True) -> List[Dict]:
        """Obtiene todas las áreas"""
        return self.db.get_all_areas(active_only)

    def update_area(self, area_id: int, **kwargs) -> bool:
        """Actualiza un área"""
        success = self.db.update_area(area_id, **kwargs)

        if success:
            # Invalidar caché de esta área
            if area_id in self._areas_cache:
                del self._areas_cache[area_id]

            # Obtener área actualizada y emitir señal
            area = self.get_area(area_id)
            if area:
                self.area_updated.emit(area)

            logger.info(f"Área {area_id} actualizada")

        return success

    def delete_area(self, area_id: int) -> bool:
        """Elimina un área"""
        success = self.db.delete_area(area_id)

        if success:
            # Remover del caché
            if area_id in self._areas_cache:
                del self._areas_cache[area_id]

            self.area_deleted.emit(area_id)
            logger.info(f"Área {area_id} eliminada")

        return success

    # ==================== RELACIONES ====================

    def add_entity_to_area(self, area_id: int, entity_type: str,
                             entity_id: int, description: str = "",
                             order_index: int = None) -> bool:
        """
        Agrega una entidad al área

        Args:
            area_id: ID del área
            entity_type: Tipo de entidad
            entity_id: ID de la entidad
            description: Descripción contextual
            order_index: Índice de orden (None = al final)

        Returns:
            True si se agregó exitosamente
        """
        # Validar tipo de entidad
        if not validate_entity_type(entity_type):
            logger.error(f"Tipo de entidad inválido: {entity_type}")
            return False

        # Si no se especifica orden, agregar al final
        if order_index is None:
            # Obtener el order_index máximo actual
            relations = self.db.get_area_relations(area_id)
            components = self.db.get_area_components(area_id)

            max_order = -1
            for rel in relations:
                rel_order = rel.get('order_index')
                # Manejar None explícitamente
                if rel_order is not None and rel_order > max_order:
                    max_order = rel_order
            for comp in components:
                comp_order = comp.get('order_index')
                # Manejar None explícitamente
                if comp_order is not None and comp_order > max_order:
                    max_order = comp_order

            order_index = max_order + 1

        try:
            relation_id = self.db.add_area_relation(
                area_id, entity_type, entity_id, description, order_index
            )

            if relation_id:
                self.relation_added.emit(area_id, entity_type, entity_id)
                logger.info(f"Entidad agregada: {entity_type}#{entity_id} -> Área#{area_id}")
                return True

            return False

        except Exception as e:
            logger.error(f"Error agregando entidad al área: {e}")
            return False

    def remove_entity_from_area(self, area_id: int, entity_type: str,
                                   entity_id: int) -> bool:
        """Elimina una entidad del área"""
        success = self.db.remove_area_relation_by_entity(
            area_id, entity_type, entity_id
        )

        if success:
            self.relation_removed.emit(area_id, entity_type, entity_id)

        return success

    def add_component_to_area(self, area_id: int, component_type: str,
                                content: str = "", order_index: int = None) -> bool:
        """Agrega un componente estructural al área"""
        if order_index is None:
            relations = self.db.get_area_relations(area_id)
            components = self.db.get_area_components(area_id)
            order_index = len(relations) + len(components)

        try:
            component_id = self.db.add_area_component(
                area_id, component_type, content, order_index
            )

            if component_id:
                self.component_added.emit(area_id, component_type)
                return True

            return False

        except Exception as e:
            logger.error(f"Error agregando componente: {e}")
            return False

    # ==================== UTILIDADES ====================

    def get_area_entities_grouped(self, area_id: int) -> Dict[str, List]:
        """
        Obtiene todas las entidades del área agrupadas por tipo

        Returns:
            Diccionario con listas por tipo de entidad
        """
        relations = self.db.get_area_relations(area_id)

        grouped = {
            'tags': [],
            'processes': [],
            'lists': [],
            'tables': [],
            'categories': [],
            'items': []
        }

        for rel in relations:
            entity_type = rel['entity_type']
            key = entity_type + 's'  # 'tag' -> 'tags'
            if key in grouped:
                grouped[key].append(rel)

        return grouped

    def get_entity_metadata(self, entity_type: str, entity_id: int) -> Dict:
        """
        Obtiene metadata de una entidad (nombre, icono, etc)

        Returns:
            Diccionario con metadata de la entidad
        """
        from src.models.area import get_entity_type_icon, get_entity_type_label

        metadata = {
            'type': entity_type,
            'id': entity_id,
            'icon': get_entity_type_icon(entity_type),
            'label': get_entity_type_label(entity_type),
            'name': '',
            'content': ''
        }

        # Obtener nombre/contenido desde BD
        try:
            if entity_type == 'tag':
                result = self.db.execute_query(
                    "SELECT name FROM tags WHERE id = ?", (entity_id,)
                )
                if result:
                    metadata['name'] = result[0]['name']

            elif entity_type == 'item':
                result = self.db.execute_query(
                    "SELECT label, content FROM items WHERE id = ?", (entity_id,)
                )
                if result:
                    metadata['name'] = result[0]['label']
                    metadata['content'] = result[0]['content']

            elif entity_type == 'list':
                result = self.db.execute_query(
                    "SELECT name FROM listas WHERE id = ?", (entity_id,)
                )
                if result:
                    metadata['name'] = result[0]['name']

            elif entity_type == 'process':
                result = self.db.execute_query(
                    "SELECT name FROM processes WHERE id = ?", (entity_id,)
                )
                if result:
                    metadata['name'] = result[0]['name']

            elif entity_type == 'table':
                result = self.db.execute_query(
                    "SELECT name FROM tables WHERE id = ?", (entity_id,)
                )
                if result:
                    metadata['name'] = result[0]['name']

            elif entity_type == 'category':
                result = self.db.execute_query(
                    "SELECT name FROM categories WHERE id = ?", (entity_id,)
                )
                if result:
                    metadata['name'] = result[0]['name']

        except Exception as e:
            logger.error(f"Error obteniendo metadata de {entity_type}#{entity_id}: {e}")

        return metadata

    def validate_area_name(self, name: str, exclude_id: int = None) -> Tuple[bool, str]:
        """
        Valida el nombre del área

        Returns:
            Tupla (es_valido, mensaje_error)
        """
        if not name or not name.strip():
            return False, "El nombre no puede estar vacío"

        if len(name) > 100:
            return False, "El nombre es demasiado largo (máx 100 caracteres)"

        # Verificar unicidad
        all_areas = self.db.get_all_areas(active_only=False)
        for area in all_areas:
            if area['name'].lower() == name.lower():
                if exclude_id is None or area['id'] != exclude_id:
                    return False, f"Ya existe un área con el nombre '{name}'"

        return True, ""

    def duplicate_area(self, area_id: int, new_name: str = None) -> Optional[Dict]:
        """
        Duplica un área con todas sus relaciones y componentes

        Args:
            area_id: ID del área a duplicar
            new_name: Nombre de la nueva área (None = auto-generar)

        Returns:
            Área duplicada o None si falla
        """
        # Obtener área original
        original = self.db.get_area(area_id)
        if not original:
            logger.error(f"Área {area_id} no encontrada")
            return None

        # Generar nombre si no se especifica
        if not new_name:
            new_name = f"{original['name']} (Copia)"

        # Crear nueva área
        new_area = self.create_area(
            name=new_name,
            description=original['description'],
            color=original['color'],
            icon=original['icon']
        )

        if not new_area:
            return None

        new_area_id = new_area['id']

        # Copiar relaciones
        relations = self.db.get_area_relations(area_id)
        for rel in relations:
            self.db.add_area_relation(
                new_area_id,
                rel['entity_type'],
                rel['entity_id'],
                rel['description'],
                rel['order_index']
            )

        # Copiar componentes
        components = self.db.get_area_components(area_id)
        for comp in components:
            self.db.add_area_component(
                new_area_id,
                comp['component_type'],
                comp['content'],
                comp['order_index']
            )

        logger.info(f"Área duplicada: {original['name']} -> {new_name}")
        return new_area

    def get_area_summary(self, area_id: int) -> Dict[str, Any]:
        """Obtiene resumen completo del área"""
        return self.db.get_area_summary(area_id)

    def search_areas(self, query: str) -> List[Dict]:
        """Busca áreas por nombre o descripción"""
        return self.db.search_areas(query)
