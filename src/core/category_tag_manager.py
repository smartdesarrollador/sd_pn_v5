# -*- coding: utf-8 -*-
"""
Category Tag Manager - Gestor de tags para categorías

Maneja la creación, búsqueda y gestión de tags específicos para categorías.
Los tags de categorías son diferentes de los tags de items/projects.
"""

import logging
from typing import List, Optional
from src.models.category_tag import CategoryTag

logger = logging.getLogger(__name__)


class CategoryTagManager:
    """
    Manager para gestionar tags de categorías

    Proporciona operaciones CRUD y búsqueda de tags específicos para categorías.
    Los tags se almacenan en la tabla `category_tags`.
    """

    def __init__(self, db):
        """
        Inicializar Category Tag Manager

        Args:
            db: DBManager instance
        """
        self.db = db
        logger.info("CategoryTagManager initialized")

    def get_all_tags(self) -> List[CategoryTag]:
        """
        Obtener todos los tags de categorías

        Returns:
            List[CategoryTag]: Lista de tags ordenados alfabéticamente
        """
        try:
            tags_data = self.db.get_all_category_tags()
            tags = [
                CategoryTag(
                    id=tag['id'],
                    name=tag['name'],
                    created_at=tag.get('created_at'),
                    updated_at=tag.get('updated_at')
                )
                for tag in tags_data
            ]
            return tags
        except Exception as e:
            logger.error(f"Error getting all category tags: {e}")
            return []

    def get_tag(self, tag_id: int) -> Optional[CategoryTag]:
        """
        Obtener tag por ID

        Args:
            tag_id: ID del tag

        Returns:
            CategoryTag o None si no se encuentra
        """
        try:
            all_tags = self.get_all_tags()
            for tag in all_tags:
                if tag.id == tag_id:
                    return tag
            return None
        except Exception as e:
            logger.error(f"Error getting category tag {tag_id}: {e}")
            return None

    def get_tag_by_name(self, name: str) -> Optional[CategoryTag]:
        """
        Obtener tag por nombre

        Args:
            name: Nombre del tag

        Returns:
            CategoryTag o None si no se encuentra
        """
        try:
            name = name.strip().lower()
            all_tags = self.get_all_tags()
            for tag in all_tags:
                if tag.name.lower() == name:
                    return tag
            return None
        except Exception as e:
            logger.error(f"Error getting category tag by name '{name}': {e}")
            return None

    def create_tag(self, name: str, color: str = "#3498db") -> Optional[CategoryTag]:
        """
        Crear o obtener un tag existente

        Args:
            name: Nombre del tag
            color: Color del tag (no se almacena en BD, solo para UI)

        Returns:
            CategoryTag creado o existente
        """
        try:
            name = name.strip().lower()

            if not name:
                logger.warning("Cannot create tag with empty name")
                return None

            # Intentar obtener tag existente
            existing_tag = self.get_tag_by_name(name)
            if existing_tag:
                return existing_tag

            # Crear nuevo tag en la BD
            tag_id = self.db.get_or_create_category_tag(name)

            if tag_id:
                return CategoryTag(
                    id=tag_id,
                    name=name,
                    color=color
                )

            return None

        except Exception as e:
            logger.error(f"Error creating category tag '{name}': {e}")
            return None

    def search_tags(self, query: str) -> List[CategoryTag]:
        """
        Buscar tags por nombre (fuzzy search)

        Args:
            query: Texto de búsqueda

        Returns:
            List[CategoryTag]: Lista de tags que coinciden
        """
        try:
            if not query:
                return self.get_all_tags()

            query = query.lower()
            all_tags = self.get_all_tags()

            # Buscar tags que contengan el query
            matching_tags = [
                tag for tag in all_tags
                if query in tag.name.lower()
            ]

            return matching_tags

        except Exception as e:
            logger.error(f"Error searching category tags for '{query}': {e}")
            return []

    def delete_unused_tags(self) -> int:
        """
        Eliminar tags que no están asociados a ninguna categoría

        Returns:
            int: Número de tags eliminados
        """
        try:
            return self.db.delete_unused_category_tags()
        except Exception as e:
            logger.error(f"Error deleting unused category tags: {e}")
            return 0
