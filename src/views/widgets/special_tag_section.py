"""
Special Tag Section
Campo para tag especial que se relaciona con proyecto/área
Se deshabilita automáticamente si el checkbox "Crear como lista" está marcado
"""

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit
from PyQt6.QtCore import pyqtSignal, Qt
from PyQt6.QtGui import QFont
import logging

logger = logging.getLogger(__name__)


class SpecialTagSection(QWidget):
    """
    Sección para tag especial (relacionado con proyecto/área)

    Características:
    - Campo de texto simple (no selector múltiple)
    - Se deshabilita si checkbox "Crear como lista" está marcado
    - Obligatorio si hay proyecto/área seleccionado (y no es lista)

    Señales:
        tag_changed(str): Emitida cuando cambia el texto del tag
    """

    # Señales
    tag_changed = pyqtSignal(str)

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
        header_label = QLabel("🔗 Tag de Relación con Proyecto")
        header_label.setFont(QFont("Segoe UI", 10, QFont.Weight.Bold))
        header_label.setStyleSheet("color: #ffffff;")
        header_layout.addWidget(header_label)

        # Info icon con tooltip
        info_label = QLabel("ℹ️")
        info_label.setToolTip(
            "Tag especial que vincula estos items con el proyecto seleccionado.\n"
            "Este tag se guardará en la tabla 'project_relations'.\n"
            "Obligatorio si hay proyecto/área seleccionado."
        )
        info_label.setStyleSheet("color: #888; font-size: 12px;")
        header_layout.addWidget(info_label)
        header_layout.addStretch()

        main_layout.addLayout(header_layout)

        # Campo de texto
        field_layout = QHBoxLayout()
        field_layout.setSpacing(6)

        label = QLabel("Tag:")
        label.setFixedWidth(80)
        label.setStyleSheet("color: #cccccc; font-size: 11px;")
        field_layout.addWidget(label)

        self.tag_input = QLineEdit()
        self.tag_input.setPlaceholderText("Ej: backend, frontend, database...")
        self.tag_input.textChanged.connect(self._on_text_changed)
        field_layout.addWidget(self.tag_input)

        main_layout.addLayout(field_layout)

        # Label de estado
        self.status_label = QLabel("")
        self.status_label.setStyleSheet("color: #888; font-size: 10px; font-style: italic;")
        main_layout.addWidget(self.status_label)

    def _apply_styles(self):
        """Aplica estilos CSS"""
        self.setStyleSheet("""
            SpecialTagSection {
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
            QLineEdit:disabled {
                background-color: #1a1a1a;
                color: #666;
                border: 1px solid #333;
            }
            QLineEdit::placeholder {
                color: #666;
            }
        """)

    def _on_text_changed(self, text: str):
        """Callback cuando cambia el texto"""
        self.tag_changed.emit(text.strip())
        logger.debug(f"Tag especial cambiado: '{text.strip()}'")

    def get_tag(self) -> str:
        """Obtiene el tag actual"""
        return self.tag_input.text().strip()

    def set_tag(self, tag: str):
        """
        Establece el tag

        Args:
            tag: Nombre del tag
        """
        self.tag_input.setText(tag)
        logger.debug(f"Tag especial establecido: '{tag}'")

    def clear(self):
        """Limpia el campo"""
        self.tag_input.clear()
        self.status_label.clear()

    def set_enabled(self, enabled: bool):
        """
        Habilita/deshabilita el campo

        Args:
            enabled: True para habilitar, False para deshabilitar
        """
        self.tag_input.setEnabled(enabled)

        if not enabled:
            self.status_label.setText("⚠️ Deshabilitado: La lista tomará el lugar del tag especial")
            self.status_label.setStyleSheet("color: #FFA726; font-size: 10px; font-style: italic;")
        else:
            self.status_label.clear()

        logger.debug(f"Tag especial {'habilitado' if enabled else 'deshabilitado'}")

    def is_enabled(self) -> bool:
        """Verifica si el campo está habilitado"""
        return self.tag_input.isEnabled()

    def validate(self, project_or_area_selected: bool, is_list: bool) -> tuple[bool, str]:
        """
        Valida el tag especial

        Args:
            project_or_area_selected: Si hay proyecto o área seleccionado
            is_list: Si el checkbox "Crear como lista" está marcado

        Returns:
            Tupla (is_valid, error_message)
        """
        # Si no hay proyecto/área, no es obligatorio
        if not project_or_area_selected:
            return True, ""

        # Si es lista, no es obligatorio (está deshabilitado)
        if is_list:
            return True, ""

        # Si hay proyecto/área y NO es lista, es obligatorio
        tag = self.get_tag()
        if not tag:
            return False, "El tag de relación es obligatorio cuando hay proyecto/área seleccionado"

        if len(tag) < 2:
            return False, "El tag debe tener al menos 2 caracteres"

        if len(tag) > 50:
            return False, "El tag no puede tener más de 50 caracteres"

        return True, ""
