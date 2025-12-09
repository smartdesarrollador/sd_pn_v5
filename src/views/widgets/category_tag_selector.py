"""
Category Tag Selector Widget - Selector multi-tag con autocompletado para categorías

Widget para seleccionar múltiples tags de categorías con búsqueda en tiempo real
y visualización como chips.
"""

from typing import List
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLineEdit,
    QListWidget, QListWidgetItem, QFrame, QScrollArea
)
from PyQt6.QtCore import pyqtSignal, Qt, QTimer
from PyQt6.QtGui import QFont

from src.core.category_tag_manager import CategoryTagManager
from src.models.category_tag import CategoryTag
from src.views.widgets.category_tag_chip import CategoryTagChip


class CategoryTagSelector(QWidget):
    """
    Selector de múltiples tags de categorías con autocompletado

    Permite buscar y seleccionar tags mostrándolos como chips.
    Incluye búsqueda en tiempo real y creación rápida de tags.
    """

    # Señales
    tags_changed = pyqtSignal(list)  # List[int] tag IDs

    def __init__(self, tag_manager: CategoryTagManager, parent=None):
        """
        Inicializa el selector

        Args:
            tag_manager: Manager de category tags
            parent: Widget padre
        """
        super().__init__(parent)
        self.tag_manager = tag_manager
        self.selected_tags: List[CategoryTag] = []
        self._search_timer = QTimer()
        self._search_timer.setSingleShot(True)
        self._search_timer.timeout.connect(self._perform_search)
        self._setup_ui()

    def _setup_ui(self):
        """Configura la UI del selector"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(8)

        # Área de chips seleccionados
        self.chips_frame = QFrame()
        self.chips_frame.setMaximumHeight(100)
        self.chips_layout = QHBoxLayout(self.chips_frame)
        self.chips_layout.setContentsMargins(4, 4, 4, 4)
        self.chips_layout.setSpacing(4)
        self.chips_layout.addStretch()

        # Scroll para chips
        scroll = QScrollArea()
        scroll.setWidget(self.chips_frame)
        scroll.setWidgetResizable(True)
        scroll.setMaximumHeight(110)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        layout.addWidget(scroll)

        # Campo de búsqueda
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("🔍 Buscar o crear tag...")
        self.search_input.setFont(QFont("Segoe UI", 10))
        self.search_input.textChanged.connect(self._on_search_text_changed)
        self.search_input.returnPressed.connect(self._on_enter_pressed)
        layout.addWidget(self.search_input)

        # Lista de resultados
        self.results_list = QListWidget()
        self.results_list.setFont(QFont("Segoe UI", 9))
        self.results_list.setMaximumHeight(200)
        self.results_list.itemClicked.connect(self._on_tag_selected)
        self.results_list.hide()
        layout.addWidget(self.results_list)

        self._apply_styles()

    def _apply_styles(self):
        """Aplica estilos CSS"""
        self.search_input.setStyleSheet("""
            QLineEdit {
                padding: 8px;
                border: 2px solid #3498db;
                border-radius: 6px;
                background-color: #2c3e50;
                color: #ecf0f1;
                font-size: 10pt;
            }
            QLineEdit:focus {
                border: 2px solid #5dade2;
            }
        """)

        self.results_list.setStyleSheet("""
            QListWidget {
                background-color: #34495e;
                color: #ecf0f1;
                border: 1px solid #3498db;
                border-radius: 6px;
                padding: 4px;
            }
            QListWidget::item {
                padding: 8px;
                border-radius: 4px;
            }
            QListWidget::item:hover {
                background-color: #3498db;
            }
            QListWidget::item:selected {
                background-color: #2980b9;
            }
        """)

        self.chips_frame.setStyleSheet("""
            QFrame {
                background-color: #2c3e50;
                border: 1px solid #34495e;
                border-radius: 6px;
            }
        """)

    def _on_search_text_changed(self, text: str):
        """Maneja cambio en texto de búsqueda (con debounce)"""
        self._search_timer.stop()
        self._search_timer.start(300)  # 300ms debounce

    def _perform_search(self):
        """Realiza la búsqueda de tags"""
        query = self.search_input.text().strip()

        if not query:
            self.results_list.hide()
            return

        # Buscar tags
        results = self.tag_manager.search_tags(query)

        # Filtrar tags ya seleccionados
        selected_ids = [tag.id for tag in self.selected_tags]
        results = [tag for tag in results if tag.id not in selected_ids]

        # Mostrar resultados
        self.results_list.clear()

        if results:
            for tag in results[:10]:  # Máximo 10 resultados
                item = QListWidgetItem(f"{tag.name}")
                item.setData(Qt.ItemDataRole.UserRole, tag)
                self.results_list.addItem(item)
            self.results_list.show()
        else:
            # Opción para crear nuevo tag
            item = QListWidgetItem(f"✨ Crear tag: '{query}'")
            item.setData(Qt.ItemDataRole.UserRole, None)
            self.results_list.addItem(item)
            self.results_list.show()

    def _on_tag_selected(self, item: QListWidgetItem):
        """Maneja selección de tag de la lista"""
        tag = item.data(Qt.ItemDataRole.UserRole)

        if tag is None:
            # Crear nuevo tag
            query = self.search_input.text().strip()
            tag = self.tag_manager.create_tag(name=query, color="#3498db")

            if not tag:
                return

        # Agregar tag a seleccionados
        if tag.id not in [t.id for t in self.selected_tags]:
            self.selected_tags.append(tag)
            self._add_chip(tag)
            self.tags_changed.emit([t.id for t in self.selected_tags])

        # Limpiar búsqueda
        self.search_input.clear()
        self.results_list.hide()

    def _on_enter_pressed(self):
        """Maneja presión de Enter en búsqueda"""
        if self.results_list.count() > 0:
            # Seleccionar primer resultado
            first_item = self.results_list.item(0)
            self._on_tag_selected(first_item)

    def _add_chip(self, tag: CategoryTag):
        """Agrega un chip de tag a la vista"""
        chip = CategoryTagChip(tag, removable=True)
        chip.tag_removed.connect(self._on_chip_removed)

        # Insertar antes del stretch
        self.chips_layout.insertWidget(self.chips_layout.count() - 1, chip)

    def _on_chip_removed(self, tag_id: int):
        """Maneja remoción de chip"""
        # Remover tag de seleccionados
        self.selected_tags = [t for t in self.selected_tags if t.id != tag_id]

        # Remover chip visual
        for i in range(self.chips_layout.count()):
            widget = self.chips_layout.itemAt(i).widget()
            if isinstance(widget, CategoryTagChip) and widget.tag.id == tag_id:
                widget.deleteLater()
                break

        self.tags_changed.emit([t.id for t in self.selected_tags])

    def set_selected_tags(self, tag_ids: List[int]):
        """
        Establece los tags seleccionados

        Args:
            tag_ids: Lista de IDs de tags a seleccionar
        """
        # Limpiar selección actual
        self.clear_selection()

        # Cargar tags
        for tag_id in tag_ids:
            tag = self.tag_manager.get_tag(tag_id)
            if tag:
                self.selected_tags.append(tag)
                self._add_chip(tag)

    def get_selected_tags(self) -> List[int]:
        """
        Obtiene los IDs de tags seleccionados

        Returns:
            Lista de IDs de tags
        """
        return [tag.id for tag in self.selected_tags]

    def get_selected_tag_names(self) -> List[str]:
        """
        Obtiene los nombres de tags seleccionados

        Returns:
            Lista de nombres de tags
        """
        return [tag.name for tag in self.selected_tags]

    def clear_selection(self):
        """Limpia la selección de tags"""
        self.selected_tags.clear()

        # Remover todos los chips
        while self.chips_layout.count() > 1:  # Dejar el stretch
            item = self.chips_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        self.search_input.clear()
        self.results_list.hide()
