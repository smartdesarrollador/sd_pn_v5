"""
Area List Widget - Lista de áreas con búsqueda

Widget que muestra una lista de áreas disponibles con capacidad de
búsqueda, selección y gestión básica.
"""

from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                             QLineEdit, QListWidget, QListWidgetItem,
                             QPushButton, QFrame)
from PyQt6.QtCore import pyqtSignal, Qt
from PyQt6.QtGui import QFont
import logging

logger = logging.getLogger(__name__)


class AreaListWidget(QWidget):
    """
    Widget de lista de áreas

    Muestra áreas disponibles con búsqueda en tiempo real y
    permite selección para ver detalles.
    """

    # Señales
    area_selected = pyqtSignal(int)  # area_id
    new_area_requested = pyqtSignal()
    search_changed = pyqtSignal(str)

    def __init__(self, parent=None):
        """
        Inicializa el widget

        Args:
            parent: Widget padre
        """
        super().__init__(parent)

        self._setup_ui()
        logger.info("AreaListWidget initialized")

    def _setup_ui(self):
        """Configura la UI del widget"""
        # Layout principal
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)

        # Header
        header = QLabel("🏢 Mis Áreas")
        header.setFont(QFont("Segoe UI", 14, QFont.Weight.Bold))
        header.setStyleSheet("color: #ffffff; padding: 10px;")
        layout.addWidget(header)

        # Búsqueda
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("🔍 Buscar áreas...")
        self.search_input.setFont(QFont("Segoe UI", 10))
        self.search_input.textChanged.connect(self._on_search_changed)
        layout.addWidget(self.search_input)

        # Botón nuevo área
        self.new_btn = QPushButton("+ Nueva Área")
        self.new_btn.setFont(QFont("Segoe UI", 10))
        self.new_btn.clicked.connect(self._on_new_area)
        layout.addWidget(self.new_btn)

        # Botones de importar/exportar
        import_export_layout = QHBoxLayout()

        self.import_btn = QPushButton("📥 Importar")
        self.import_btn.setFont(QFont("Segoe UI", 9))
        self.import_btn.setToolTip("Importar área desde JSON")
        import_export_layout.addWidget(self.import_btn)

        self.export_btn = QPushButton("📤 Exportar")
        self.export_btn.setFont(QFont("Segoe UI", 9))
        self.export_btn.setToolTip("Exportar área seleccionada a JSON")
        import_export_layout.addWidget(self.export_btn)

        layout.addLayout(import_export_layout)

        # Lista de áreas
        self.areas_list = QListWidget()
        self.areas_list.itemClicked.connect(self._on_area_clicked)
        layout.addWidget(self.areas_list)

        # Aplicar estilos
        self._apply_styles()

    def _apply_styles(self):
        """Aplica estilos al widget"""
        # Estilo general del widget
        self.setStyleSheet("""
            QWidget {
                background-color: #252525;
                border-right: 2px solid #3d3d3d;
            }
        """)

        # Estilo del input de búsqueda
        self.search_input.setStyleSheet("""
            QLineEdit {
                background-color: #2d2d2d;
                color: #ffffff;
                border: 1px solid #3d3d3d;
                padding: 8px;
                border-radius: 4px;
            }
            QLineEdit:focus {
                border: 1px solid #9b59b6;
            }
        """)

        # Estilo de botones
        button_style = """
            QPushButton {
                background-color: #2d2d2d;
                color: #ffffff;
                border: 1px solid #3d3d3d;
                padding: 8px 16px;
                border-radius: 4px;
                font-size: 10pt;
            }
            QPushButton:hover {
                background-color: #3d3d3d;
                border-color: #9b59b6;
            }
            QPushButton:pressed {
                background-color: #1e1e1e;
            }
        """
        self.new_btn.setStyleSheet(button_style)
        self.import_btn.setStyleSheet(button_style)
        self.export_btn.setStyleSheet(button_style)

        # Estilo de la lista
        self.areas_list.setStyleSheet("""
            QListWidget {
                background-color: #2d2d2d;
                color: #ffffff;
                border: 1px solid #3d3d3d;
                border-radius: 4px;
                font-size: 10pt;
            }
            QListWidget::item {
                padding: 10px;
                border-bottom: 1px solid #3d3d3d;
            }
            QListWidget::item:selected {
                background-color: #9b59b6;
                color: #000000;
            }
            QListWidget::item:hover {
                background-color: #3d3d3d;
            }
        """)

    def load_areas(self, areas: list):
        """
        Carga áreas en la lista

        Args:
            areas: Lista de diccionarios con datos de áreas
                   Cada área debe tener: id, name, icon
        """
        self.areas_list.clear()

        for area in areas:
            icon = area.get('icon', '🏢')
            name = area.get('name', 'Sin nombre')
            area_id = area.get('id')

            item = QListWidgetItem(f"{icon} {name}")
            item.setData(Qt.ItemDataRole.UserRole, area_id)
            self.areas_list.addItem(item)

        logger.info(f"Loaded {len(areas)} areas")

    def clear(self):
        """Limpia la lista de áreas"""
        self.areas_list.clear()
        logger.debug("Areas list cleared")

    def get_selected_area_id(self) -> int:
        """
        Obtiene el ID del área seleccionada

        Returns:
            ID del área seleccionada o None si no hay selección
        """
        current_item = self.areas_list.currentItem()
        if current_item:
            return current_item.data(Qt.ItemDataRole.UserRole)
        return None

    def select_area(self, area_id: int):
        """
        Selecciona un área por ID

        Args:
            area_id: ID del área a seleccionar
        """
        for i in range(self.areas_list.count()):
            item = self.areas_list.item(i)
            if item.data(Qt.ItemDataRole.UserRole) == area_id:
                self.areas_list.setCurrentItem(item)
                logger.debug(f"Area {area_id} selected")
                break

    def _on_area_clicked(self, item: QListWidgetItem):
        """
        Maneja click en área de la lista

        Args:
            item: Item clickeado
        """
        area_id = item.data(Qt.ItemDataRole.UserRole)
        if area_id:
            self.area_selected.emit(area_id)
            logger.debug(f"Area clicked: {area_id}")

    def _on_new_area(self):
        """Maneja click en botón de nueva área"""
        self.new_area_requested.emit()
        logger.debug("New area requested")

    def _on_search_changed(self, text: str):
        """
        Maneja cambio en búsqueda

        Args:
            text: Texto de búsqueda
        """
        self.search_changed.emit(text)
        logger.debug(f"Search changed: {text}")

    def filter_areas(self, search_text: str, all_areas: list):
        """
        Filtra áreas por texto de búsqueda

        Args:
            search_text: Texto a buscar
            all_areas: Lista completa de áreas
        """
        if not search_text:
            self.load_areas(all_areas)
            return

        search_text = search_text.lower()
        filtered = [
            area for area in all_areas
            if search_text in area.get('name', '').lower() or
               search_text in area.get('description', '').lower()
        ]

        self.load_areas(filtered)
        logger.debug(f"Filtered areas: {len(filtered)} of {len(all_areas)}")
