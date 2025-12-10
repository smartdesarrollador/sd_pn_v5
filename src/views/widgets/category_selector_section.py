"""
Category Selector Section
Sección independiente para selector de categoría con botón de creación
"""

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QComboBox, QPushButton
from PyQt6.QtCore import pyqtSignal, Qt
from PyQt6.QtGui import QFont
import logging

logger = logging.getLogger(__name__)


class CategorySelectorSection(QWidget):
    """
    Sección para seleccionar o crear categoría

    Señales:
        category_changed(int | None): Emitida cuando cambia la categoría seleccionada
        create_category_clicked(): Emitida cuando se hace clic en botón "+"
    """

    # Señales
    category_changed = pyqtSignal(object)  # int | None
    create_category_clicked = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self._setup_ui()
        self._apply_styles()

    def _setup_ui(self):
        """Configura la interfaz"""
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(15, 10, 15, 10)
        main_layout.setSpacing(8)

        # Header
        header_label = QLabel("📁 Categoría")
        header_label.setFont(QFont("Segoe UI", 10, QFont.Weight.Bold))
        header_label.setStyleSheet("color: #ffffff;")
        main_layout.addWidget(header_label)

        # Layout horizontal para selector + botón
        selector_layout = QHBoxLayout()
        selector_layout.setSpacing(6)

        # Label
        label = QLabel("Categoría:*")
        label.setFixedWidth(80)
        label.setStyleSheet("color: #cccccc; font-size: 11px;")
        selector_layout.addWidget(label)

        # ComboBox
        self.category_combo = QComboBox()
        self.category_combo.addItem("Seleccionar categoría...", None)
        self.category_combo.currentIndexChanged.connect(self._on_category_changed)
        selector_layout.addWidget(self.category_combo)

        # Botón "+"
        self.create_btn = QPushButton("+")
        self.create_btn.setFixedSize(28, 28)
        self.create_btn.setToolTip("Crear nueva categoría")
        self.create_btn.clicked.connect(self.create_category_clicked.emit)
        selector_layout.addWidget(self.create_btn)

        main_layout.addLayout(selector_layout)

    def _apply_styles(self):
        """Aplica estilos CSS"""
        self.setStyleSheet("""
            CategorySelectorSection {
                background-color: #252525;
                border-radius: 6px;
            }
            QComboBox {
                background-color: #2d2d2d;
                color: #ffffff;
                border: 1px solid #444;
                border-radius: 4px;
                padding: 6px 10px;
                font-size: 11px;
                min-height: 24px;
            }
            QComboBox:hover {
                border: 1px solid #2196F3;
            }
            QComboBox::drop-down {
                border: none;
                width: 20px;
            }
            QComboBox::down-arrow {
                image: none;
                border-left: 4px solid transparent;
                border-right: 4px solid transparent;
                border-top: 5px solid #aaa;
                margin-right: 6px;
            }
            QComboBox QAbstractItemView {
                background-color: #2d2d2d;
                color: #ffffff;
                selection-background-color: #2196F3;
                border: 1px solid #444;
            }
            QPushButton {
                background-color: #2196F3;
                color: #ffffff;
                border: none;
                border-radius: 4px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #1976D2;
            }
            QPushButton:pressed {
                background-color: #0D47A1;
            }
        """)

    def _on_category_changed(self, index: int):
        """Callback cuando cambia la selección"""
        category_id = self.category_combo.currentData()
        self.category_changed.emit(category_id)
        logger.debug(f"Categoría cambiada: {category_id}")

    def load_categories(self, categories: list[tuple[int, str]]):
        """
        Carga categorías disponibles en el selector

        Args:
            categories: Lista de tuplas (id, nombre)
        """
        self.category_combo.clear()
        self.category_combo.addItem("Seleccionar categoría...", None)

        for cat_id, cat_name in categories:
            self.category_combo.addItem(cat_name, cat_id)

        logger.debug(f"Cargadas {len(categories)} categorías")

    def get_category_id(self) -> int | None:
        """Obtiene el ID de la categoría seleccionada"""
        return self.category_combo.currentData()

    def set_category_id(self, category_id: int | None):
        """
        Establece la categoría seleccionada

        Args:
            category_id: ID de la categoría a seleccionar
        """
        if category_id is None:
            self.category_combo.setCurrentIndex(0)
            return

        for i in range(self.category_combo.count()):
            if self.category_combo.itemData(i) == category_id:
                self.category_combo.setCurrentIndex(i)
                logger.debug(f"Categoría seleccionada: {category_id}")
                return

        logger.warning(f"Categoría {category_id} no encontrada en selector")

    def clear(self):
        """Limpia la selección"""
        self.category_combo.setCurrentIndex(0)

    def validate(self) -> tuple[bool, str]:
        """
        Valida que se haya seleccionado una categoría

        Returns:
            Tupla (is_valid, error_message)
        """
        if self.get_category_id() is None:
            return False, "Debe seleccionar una categoría"
        return True, ""
