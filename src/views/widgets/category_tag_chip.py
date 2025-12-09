"""
Category Tag Chip Widget - Widget visual para mostrar un tag individual de categoría

Widget pequeño que muestra un tag de categoría con su color y nombre,
opcionalmente con botón para remover.
"""

from PyQt6.QtWidgets import QWidget, QHBoxLayout, QLabel, QPushButton
from PyQt6.QtCore import pyqtSignal, Qt
from PyQt6.QtGui import QFont

from src.models.category_tag import CategoryTag


class CategoryTagChip(QWidget):
    """
    Widget chip para mostrar un tag individual de categoría

    Muestra el tag con su color de fondo y nombre,
    opcionalmente con botón X para remover.
    """

    # Señales
    tag_clicked = pyqtSignal(int)  # tag_id
    tag_removed = pyqtSignal(int)  # tag_id

    def __init__(self, tag: CategoryTag, removable: bool = True, parent=None):
        """
        Inicializa el chip

        Args:
            tag: Tag a mostrar
            removable: Si True, muestra botón X para remover
            parent: Widget padre
        """
        super().__init__(parent)
        self.tag = tag
        self.removable = removable
        self._setup_ui()

    def _setup_ui(self):
        """Configura la UI del chip"""
        layout = QHBoxLayout(self)
        layout.setContentsMargins(8, 4, 8, 4)
        layout.setSpacing(4)

        # Label del nombre
        self.label = QLabel(self.tag.name)
        self.label.setFont(QFont("Segoe UI", 9))
        layout.addWidget(self.label)

        # Botón remover (opcional)
        if self.removable:
            self.remove_btn = QPushButton("×")
            self.remove_btn.setFont(QFont("Segoe UI", 12, QFont.Weight.Bold))
            self.remove_btn.setFixedSize(16, 16)
            self.remove_btn.setCursor(Qt.CursorShape.PointingHandCursor)
            self.remove_btn.clicked.connect(self._on_remove_clicked)
            layout.addWidget(self.remove_btn)

        # Aplicar estilos
        self._apply_styles()

        # Hacer clickeable
        self.setCursor(Qt.CursorShape.PointingHandCursor)

    def _apply_styles(self):
        """Aplica estilos CSS al chip"""
        # Convertir color a RGB para fondo semi-transparente
        color = self.tag.color

        # Estilos del chip
        chip_style = f"""
            CategoryTagChip {{
                background-color: {color};
                border-radius: 12px;
                border: 1px solid {color};
            }}
            CategoryTagChip:hover {{
                border: 1px solid #ffffff;
                background-color: {color}dd;
            }}
        """

        # Estilos del label
        label_style = """
            QLabel {
                color: #ffffff;
                background: transparent;
                padding: 0px;
            }
        """

        # Estilos del botón remover
        remove_style = """
            QPushButton {
                background: transparent;
                color: #ffffff;
                border: none;
                border-radius: 8px;
                padding: 0px;
            }
            QPushButton:hover {
                background-color: rgba(255, 255, 255, 0.3);
            }
        """

        self.setStyleSheet(chip_style)
        self.label.setStyleSheet(label_style)

        if self.removable:
            self.remove_btn.setStyleSheet(remove_style)

    def set_tag(self, tag: CategoryTag):
        """
        Actualiza el tag mostrado

        Args:
            tag: Nuevo tag a mostrar
        """
        self.tag = tag
        self.label.setText(tag.name)
        self._apply_styles()

    def mousePressEvent(self, event):
        """Maneja click en el chip"""
        if event.button() == Qt.MouseButton.LeftButton:
            self.tag_clicked.emit(self.tag.id)
        super().mousePressEvent(event)

    def _on_remove_clicked(self):
        """Maneja click en botón remover"""
        self.tag_removed.emit(self.tag.id)
