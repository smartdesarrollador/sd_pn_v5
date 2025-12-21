"""
Widget contenedor de grupo de items

Agrupa items bajo un encabezado de grupo (categoría, lista o tag).

Autor: Widget Sidebar Team
Versión: 1.0
"""

from PyQt6.QtWidgets import QWidget, QVBoxLayout
from PyQt6.QtCore import Qt
from .headers.group_header import GroupHeaderWidget
from .items import TextItemWidget, CodeItemWidget, URLItemWidget, PathItemWidget, WebStaticItemWidget


class ItemGroupWidget(QWidget):
    """
    Widget contenedor de grupo de items

    Agrupa items bajo un encabezado de grupo.
    Renderiza cada item con el widget apropiado según su tipo.

    Nivel de jerarquía: Grupos (categorías, listas, tags de items)
    """

    def __init__(self, group_name: str, group_type: str = "category", parent=None):
        """
        Inicializar widget de grupo de items

        Args:
            group_name: Nombre del grupo
            group_type: Tipo de grupo ('category', 'list', 'tag')
            parent: Widget padre
        """
        super().__init__(parent)

        self.group_name = group_name
        self.group_type = group_type
        self.items = []

        self.init_ui()

    def init_ui(self):
        """Inicializar interfaz de usuario"""
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        # Header del grupo
        self.header = GroupHeaderWidget()
        self.header.set_group_info(self.group_name, self.group_type)
        self.main_layout.addWidget(self.header)

        # Layout de items
        self.items_layout = QVBoxLayout()
        self.items_layout.setSpacing(0)
        self.main_layout.addLayout(self.items_layout)

    def add_item(self, item_data: dict):
        """
        Agregar item al grupo

        Crea el widget apropiado según el tipo de item
        y lo agrega al layout de items.

        Args:
            item_data: Diccionario con datos del item
        """
        item_type = item_data.get('type', 'TEXT')

        # Crear widget según tipo
        if item_type == 'CODE':
            item_widget = CodeItemWidget(item_data)
        elif item_type == 'URL':
            item_widget = URLItemWidget(item_data)
        elif item_type == 'PATH':
            item_widget = PathItemWidget(item_data)
        elif item_type == 'WEB_STATIC':
            item_widget = WebStaticItemWidget(item_data)
        else:  # TEXT o por defecto
            item_widget = TextItemWidget(item_data)

        # Conectar señal de copiado
        item_widget.item_copied.connect(self.on_item_copied)

        self.items.append(item_widget)
        self.items_layout.addWidget(item_widget)

    def on_item_copied(self, item_data: dict):
        """
        Manejar evento de item copiado

        Args:
            item_data: Datos del item copiado
        """
        label = item_data.get('label', 'Sin título')
        print(f"✓ Item copiado del grupo '{self.group_name}': {label}")

    def clear_items(self):
        """Limpiar todos los items del grupo"""
        for item in self.items:
            item.deleteLater()
        self.items.clear()

    def get_item_count(self) -> int:
        """
        Obtener cantidad de items en el grupo

        Returns:
            Número de items
        """
        return len(self.items)

    def get_group_name(self) -> str:
        """
        Obtener nombre del grupo

        Returns:
            Nombre del grupo
        """
        return self.group_name

    def get_group_type(self) -> str:
        """
        Obtener tipo del grupo

        Returns:
            Tipo del grupo
        """
        return self.group_type
