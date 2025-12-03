"""
Area Canvas Widget - Canvas scrollable para elementos de área

Widget de canvas vertical que contiene elementos del área en modo edición.
Los elementos pueden ser relaciones (tags, items, categorías, etc.) o
componentes estructurales (comentarios, notas, alertas, divisores).
"""

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QScrollArea, QFrame
from PyQt6.QtCore import pyqtSignal
import logging

logger = logging.getLogger(__name__)


class AreaCanvasWidget(QWidget):
    """
    Widget canvas para mostrar elementos del área en modo edición

    Proporciona un área scrollable donde se pueden agregar widgets de
    relaciones y componentes en orden vertical.
    """

    # Señales
    content_changed = pyqtSignal()  # Emitida cuando cambia el contenido

    def __init__(self, parent=None):
        """
        Inicializa el canvas

        Args:
            parent: Widget padre
        """
        super().__init__(parent)

        self._setup_ui()

    def _setup_ui(self):
        """Configura la UI del canvas"""
        # Layout principal
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Área scrollable
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("border: none;")

        # Widget contenedor del canvas
        self.canvas_widget = QWidget()
        self.canvas_layout = QVBoxLayout(self.canvas_widget)
        self.canvas_layout.setSpacing(5)
        self.canvas_layout.addStretch()

        scroll.setWidget(self.canvas_widget)
        main_layout.addWidget(scroll)

        logger.info("AreaCanvasWidget initialized")

    def add_widget(self, widget: QWidget):
        """
        Agrega un widget al canvas

        Args:
            widget: Widget a agregar (debe ser AreaRelationWidget o AreaComponentWidget)
        """
        # Insertar antes del stretch
        self.canvas_layout.insertWidget(self.canvas_layout.count() - 1, widget)
        self.content_changed.emit()
        logger.debug(f"Widget added to canvas: {widget.__class__.__name__}")

    def clear(self):
        """Limpia todos los widgets del canvas"""
        while self.canvas_layout.count() > 1:  # Mantener el stretch
            child = self.canvas_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        self.content_changed.emit()
        logger.debug("Canvas cleared")

    def get_widget_count(self) -> int:
        """
        Obtiene el número de widgets en el canvas

        Returns:
            Número de widgets (sin contar el stretch)
        """
        return max(0, self.canvas_layout.count() - 1)

    def get_widgets(self) -> list:
        """
        Obtiene todos los widgets del canvas

        Returns:
            Lista de widgets en el canvas
        """
        widgets = []
        for i in range(self.canvas_layout.count() - 1):  # -1 para excluir stretch
            widget = self.canvas_layout.itemAt(i).widget()
            if widget:
                widgets.append(widget)
        return widgets
