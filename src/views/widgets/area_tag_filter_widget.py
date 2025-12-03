"""
Area Tag Filter Widget - Widget para filtrar elementos por tags

Widget estilo Dashboard con lista de checkboxes de tags para filtrar
elementos de área en tiempo real.
"""

from typing import List
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QCheckBox, QScrollArea, QPushButton, QFrame
)
from PyQt6.QtCore import pyqtSignal, Qt
from PyQt6.QtGui import QFont

from src.core.area_element_tag_manager import AreaElementTagManager


class TagCheckBox(QCheckBox):
    """
    Checkbox personalizado para tags con estilos dinámicos

    Esta clase garantiza que los estilos se apliquen correctamente
    cada vez que se crea o actualiza el checkbox.
    """

    def __init__(self, tag_name: str, tag_color: str, parent=None):
        super().__init__(tag_name, parent)
        self.tag_color = tag_color
        self.setFont(QFont("Segoe UI", 9))
        self._apply_styles()

        # Conectar señal de cambio de estado para forzar actualización visual
        self.stateChanged.connect(self._on_state_changed)

    def _apply_styles(self):
        """Aplica los estilos CSS al checkbox"""
        # Estilos mejorados con indicadores visuales MUY claros
        self.setStyleSheet(f"""
            QCheckBox {{
                color: #ecf0f1;
                spacing: 8px;
                padding: 8px 12px;
                border-radius: 4px;
                background-color: #2c3e50;
                border: 1px solid transparent;
                margin: 2px 0px;
            }}
            QCheckBox:checked {{
                background-color: {self.tag_color}60;
                border: 2px solid {self.tag_color};
                font-weight: bold;
                color: #ffffff;
            }}
            QCheckBox:hover {{
                background-color: {self.tag_color}30;
                border: 1px solid {self.tag_color}80;
            }}
            QCheckBox::indicator {{
                width: 20px;
                height: 20px;
                border: 2px solid {self.tag_color}80;
                border-radius: 4px;
                background-color: #1a1a1a;
            }}
            QCheckBox::indicator:checked {{
                background-color: {self.tag_color};
                border: 3px solid {self.tag_color};
            }}
            QCheckBox::indicator:unchecked {{
                background-color: #34495e;
                border: 2px solid {self.tag_color}40;
            }}
            QCheckBox::indicator:hover {{
                border-color: {self.tag_color};
                border-width: 3px;
            }}
        """)

    def _on_state_changed(self, state):
        """Callback cuando cambia el estado - fuerza actualización visual"""
        # Forzar repaint para asegurar que los estilos se apliquen
        self.update()
        self.repaint()


class AreaTagFilterWidget(QWidget):
    """
    Widget para filtrar elementos por tags - Estilo Dashboard

    Muestra lista de tags disponibles con checkboxes para
    filtrar elementos del área.
    """

    # Señales
    filter_changed = pyqtSignal(list, bool)  # tag_ids, match_all

    def __init__(self, tag_manager: AreaElementTagManager, area_id: int = None, parent=None):
        """
        Inicializa el widget

        Args:
            tag_manager: Manager de tags
            area_id: ID del área (None = mostrar todos los tags)
            parent: Widget padre
        """
        super().__init__(parent)
        self.tag_manager = tag_manager
        self.area_id = area_id
        self.tag_checkboxes = {}  # {tag_id: TagCheckBox}
        self.match_all = False  # False = OR logic, True = AND logic
        self._setup_ui()
        self._load_tags()

        # Conectar señal de cache invalidado para refrescar
        self.tag_manager.cache_invalidated.connect(self._on_cache_invalidated)

    def _setup_ui(self):
        """Configura la UI del widget"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(8)

        # Header
        header_frame = QFrame()
        header_frame.setStyleSheet("""
            QFrame {
                background-color: #2c3e50;
                border: 1px solid #34495e;
                border-radius: 6px;
                padding: 8px;
            }
        """)
        header_layout = QVBoxLayout(header_frame)
        header_layout.setSpacing(4)

        # Título
        title = QLabel("🏷️ Filtro por Tags")
        title.setFont(QFont("Segoe UI", 11, QFont.Weight.Bold))
        title.setStyleSheet("color: #ecf0f1; background: transparent; border: none;")
        header_layout.addWidget(title)

        # Contador
        self.count_label = QLabel("(0 tags)")
        self.count_label.setFont(QFont("Segoe UI", 9))
        self.count_label.setStyleSheet("color: #95a5a6; background: transparent; border: none;")
        header_layout.addWidget(self.count_label)

        layout.addWidget(header_frame)

        # Área scrolleable de tags
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        scroll.setStyleSheet("""
            QScrollArea {
                background-color: #34495e;
                border: 1px solid #2c3e50;
                border-radius: 6px;
            }
            QScrollBar:vertical {
                background-color: #2c3e50;
                width: 10px;
                border-radius: 5px;
            }
            QScrollBar::handle:vertical {
                background-color: #7f8c8d;
                border-radius: 5px;
                min-height: 20px;
            }
            QScrollBar::handle:vertical:hover {
                background-color: #95a5a6;
            }
        """)

        # Container de checkboxes
        self.tags_container = QWidget()
        self.tags_layout = QVBoxLayout(self.tags_container)
        self.tags_layout.setContentsMargins(8, 8, 8, 8)
        self.tags_layout.setSpacing(6)
        self.tags_layout.addStretch()

        scroll.setWidget(self.tags_container)
        layout.addWidget(scroll, 1)  # Expandir

        # Checkbox "Coincidir todos"
        self.match_all_checkbox = QCheckBox("Coincidir todos (AND)")
        self.match_all_checkbox.setFont(QFont("Segoe UI", 9))
        self.match_all_checkbox.setStyleSheet("""
            QCheckBox {
                color: #ecf0f1;
                spacing: 8px;
                padding: 6px;
                background-color: #2c3e50;
                border-radius: 4px;
            }
            QCheckBox::indicator {
                width: 16px;
                height: 16px;
                border: 2px solid #7f8c8d;
                border-radius: 3px;
                background-color: #34495e;
            }
            QCheckBox::indicator:checked {
                background-color: #9b59b6;
                border-color: #9b59b6;
            }
            QCheckBox::indicator:hover {
                border-color: #bb79d6;
            }
        """)
        self.match_all_checkbox.stateChanged.connect(self._on_match_all_changed)
        layout.addWidget(self.match_all_checkbox)

        # Botones de control
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(8)

        self.select_all_btn = QPushButton("✓ Todos")
        self.select_all_btn.setFont(QFont("Segoe UI", 9))
        self.select_all_btn.clicked.connect(self._select_all)
        buttons_layout.addWidget(self.select_all_btn)

        self.select_none_btn = QPushButton("✗ Ninguno")
        self.select_none_btn.setFont(QFont("Segoe UI", 9))
        self.select_none_btn.clicked.connect(self._select_none)
        buttons_layout.addWidget(self.select_none_btn)

        layout.addLayout(buttons_layout)

        self._apply_button_styles()

    def _apply_button_styles(self):
        """Aplica estilos a los botones"""
        button_style = """
            QPushButton {
                background-color: #9b59b6;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 6px 12px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #bb79d6;
            }
            QPushButton:pressed {
                background-color: #7d3c98;
            }
        """
        self.select_all_btn.setStyleSheet(button_style)
        self.select_none_btn.setStyleSheet(button_style)

    def _load_tags(self):
        """Carga los tags disponibles"""
        # Guardar estado actual de checkboxes antes de limpiar
        current_selected = self.get_selected_tag_ids()

        # Limpiar checkboxes existentes
        for checkbox in self.tag_checkboxes.values():
            checkbox.deleteLater()
        self.tag_checkboxes.clear()

        # Remover widgets del layout (excepto el stretch)
        while self.tags_layout.count() > 1:
            item = self.tags_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        # Obtener tags según el área
        if self.area_id is not None:
            # Solo tags del área específica
            tags_sorted = self.tag_manager.get_tags_for_area(self.area_id)
        else:
            # Todos los tags
            tags = self.tag_manager.get_all_tags(refresh=True)
            tags_sorted = self.tag_manager.get_tags_sorted()

        # Actualizar contador
        self.count_label.setText(f"({len(tags_sorted)} tags)")

        # Crear checkboxes usando la clase personalizada
        for tag in tags_sorted:
            # Usar TagCheckBox personalizado que garantiza estilos correctos
            checkbox = TagCheckBox(tag.name, tag.color, parent=self.tags_container)

            # Restaurar estado si estaba seleccionado antes
            if tag.id in current_selected:
                checkbox.setChecked(True)

            # Conectar señal
            checkbox.stateChanged.connect(self._on_filter_changed)

            # Guardar referencia
            self.tag_checkboxes[tag.id] = checkbox

            # Insertar antes del stretch
            self.tags_layout.insertWidget(self.tags_layout.count() - 1, checkbox)

        # Forzar actualización del layout
        self.tags_container.updateGeometry()
        self.tags_container.update()

    def _on_filter_changed(self):
        """Maneja cambio en filtros"""
        selected_tag_ids = self.get_selected_tag_ids()
        self.filter_changed.emit(selected_tag_ids, self.match_all)

    def _on_match_all_changed(self, state):
        """Maneja cambio en checkbox de match_all"""
        self.match_all = state == Qt.CheckState.Checked.value
        self._on_filter_changed()

    def _on_cache_invalidated(self):
        """Callback cuando se invalida el caché del tag manager"""
        # Recargar tags manteniendo selección actual
        self._load_tags()

    def _select_all(self):
        """Selecciona todos los tags"""
        # Bloquear señales temporalmente para evitar múltiples emisiones
        for checkbox in self.tag_checkboxes.values():
            checkbox.blockSignals(True)
            checkbox.setChecked(True)
            checkbox.blockSignals(False)

        # Emitir señal una sola vez
        self._on_filter_changed()

    def _select_none(self):
        """Deselecciona todos los tags"""
        # Bloquear señales temporalmente para evitar múltiples emisiones
        for checkbox in self.tag_checkboxes.values():
            checkbox.blockSignals(True)
            checkbox.setChecked(False)
            checkbox.blockSignals(False)

        # Emitir señal una sola vez
        self._on_filter_changed()

    def get_selected_tag_ids(self) -> List[int]:
        """
        Obtiene los IDs de tags seleccionados

        Returns:
            Lista de IDs de tags seleccionados
        """
        return [
            tag_id for tag_id, checkbox in self.tag_checkboxes.items()
            if checkbox.isChecked()
        ]

    def set_selected_tag_ids(self, tag_ids: List[int]):
        """
        Establece los tags seleccionados

        Args:
            tag_ids: Lista de IDs de tags a seleccionar
        """
        for tag_id, checkbox in self.tag_checkboxes.items():
            checkbox.blockSignals(True)
            checkbox.setChecked(tag_id in tag_ids)
            checkbox.blockSignals(False)

        # Emitir señal una vez al final
        self._on_filter_changed()

    def clear_filters(self):
        """Limpia todos los filtros"""
        self._select_none()
        self.match_all_checkbox.setChecked(False)

    def refresh(self):
        """Refresca la lista de tags manteniendo selección"""
        self._load_tags()

    def set_area(self, area_id: int = None):
        """
        Cambia el área y recarga los tags

        Args:
            area_id: ID del área a mostrar (None = limpiar filtro)
        """
        self.area_id = area_id

        # NO limpiar filtros aquí - mantener selección del usuario
        # Solo recargar la lista de tags
        self._load_tags()
