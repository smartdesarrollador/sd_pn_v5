"""
List Name Section
Campo para nombre de lista - siempre visible y obligatorio
"""

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QFrame
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtGui import QFont
import logging

logger = logging.getLogger(__name__)


class ListNameSection(QWidget):
    """
    Sección para nombre de lista

    Características:
    - Campo de texto simple para nombre de lista
    - Siempre visible
    - Obligatorio para guardar

    Señales:
        name_changed(str): Emitida cuando cambia el texto del nombre
    """

    # Señales
    name_changed = pyqtSignal(str)

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
        header_layout = QHBoxLayout()
        header_label = QLabel("📝 Nombre de Lista")
        header_label.setFont(QFont("Segoe UI", 10, QFont.Weight.Bold))
        header_label.setStyleSheet("color: #ffffff;")
        header_layout.addWidget(header_label)

        # Badge obligatorio
        required_badge = QLabel("*")
        required_badge.setStyleSheet("color: #FF5252; font-size: 14px; font-weight: bold;")
        required_badge.setToolTip("Campo obligatorio")
        header_layout.addWidget(required_badge)

        header_layout.addStretch()

        main_layout.addLayout(header_layout)

        # Campo de texto
        field_layout = QHBoxLayout()
        field_layout.setSpacing(6)

        label = QLabel("Nombre:")
        label.setFixedWidth(80)
        label.setStyleSheet("color: #cccccc; font-size: 11px;")
        field_layout.addWidget(label)

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Ingrese el nombre de la lista...")
        self.name_input.textChanged.connect(self._on_text_changed)
        field_layout.addWidget(self.name_input)

        main_layout.addLayout(field_layout)

    def _apply_styles(self):
        """Aplica estilos CSS"""
        self.setStyleSheet("""
            ListNameSection {
                background-color: #252525;
                border-radius: 6px;
            }
            QLineEdit {
                background-color: #2d2d2d;
                color: #ffffff;
                border: 1px solid #444;
                border-radius: 4px;
                padding: 6px 10px;
                font-size: 11px;
                min-height: 24px;
            }
            QLineEdit:hover {
                border: 1px solid #2196F3;
            }
            QLineEdit:focus {
                border: 1px solid #2196F3;
                background-color: #333;
            }
            QLineEdit::placeholder {
                color: #666;
            }
        """)

    def _on_text_changed(self, text: str):
        """Callback cuando cambia el texto"""
        self.name_changed.emit(text.strip())
        logger.debug(f"Nombre de lista cambiado: '{text.strip()}'")

    def get_name(self) -> str:
        """Obtiene el nombre actual"""
        return self.name_input.text().strip()

    def set_name(self, name: str):
        """
        Establece el nombre

        Args:
            name: Nombre de la lista
        """
        self.name_input.setText(name)
        logger.debug(f"Nombre de lista establecido: '{name}'")

    def clear(self):
        """Limpia el campo"""
        self.name_input.clear()

    def validate(self) -> tuple[bool, str]:
        """
        Valida el nombre de lista

        Returns:
            Tupla (is_valid, error_message)
        """
        name = self.get_name()
        if not name:
            return False, "El nombre de lista es obligatorio"

        if len(name) < 2:
            return False, "El nombre debe tener al menos 2 caracteres"

        if len(name) > 100:
            return False, "El nombre no puede tener más de 100 caracteres"

        return True, ""
