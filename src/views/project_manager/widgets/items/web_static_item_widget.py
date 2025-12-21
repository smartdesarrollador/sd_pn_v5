"""
Widget para items de tipo WEB_STATIC

Muestra items de aplicaciones web estáticas con botón para renderizar HTML.

Autor: Widget Sidebar Team
Versión: 1.0
"""

from PyQt6.QtWidgets import QLabel, QHBoxLayout, QPushButton, QSizePolicy
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QCursor
from .base_item_widget import BaseItemWidget
from ...styles.full_view_styles import FullViewStyles
from ..common.copy_button import CopyButton
import logging

logger = logging.getLogger(__name__)


class WebStaticItemWidget(BaseItemWidget):
    """
    Widget para items de tipo WEB_STATIC

    Características:
    - Muestra código HTML sin límites
    - Botón para renderizar en navegador embebido
    - Icono 📱 para identificación visual
    """

    def __init__(self, item_data: dict, parent=None):
        """
        Inicializar widget de item web estático

        Args:
            item_data: Diccionario con datos del item
            parent: Widget padre
        """
        super().__init__(item_data, parent)
        self.apply_styles()

    def _create_action_buttons(self):
        """
        Crear botones de acción específicos para items de WEB_STATIC

        Botones:
        - Renderizar HTML (📱)
        - Copiar (siempre presente)
        """
        # Botón renderizar
        self.render_button = QPushButton("📱")
        self.render_button.setFixedSize(28, 28)
        self.render_button.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.render_button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: #ffffff;
                border: none;
                border-radius: 3px;
                font-size: 12pt;
                padding: 0px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:pressed {
                background-color: #388E3C;
            }
        """)
        self.render_button.setToolTip("Renderizar aplicación web estática")
        self.render_button.clicked.connect(self._render_web_static)
        self.buttons_layout.addWidget(self.render_button)

        # Botón de copiar
        self.copy_button = CopyButton()
        self.copy_button.copy_clicked.connect(self.copy_to_clipboard)
        self.copy_button.setFixedSize(28, 28)
        self.copy_button.setToolTip("Copiar HTML")
        self.buttons_layout.addWidget(self.copy_button)

    def _render_web_static(self):
        """Renderizar aplicación web estática"""
        try:
            # Visual feedback
            original_style = self.render_button.styleSheet()
            self.render_button.setStyleSheet("""
                QPushButton {
                    background-color: #00d4ff;
                    color: #000000;
                    border: none;
                    border-radius: 3px;
                    font-size: 12pt;
                    padding: 0px;
                }
            """)

            # Emitir señal o abrir navegador embebido
            # TODO: Implementar navegador embebido para WEB_STATIC
            logger.info(f"WEB_STATIC render requested for item: {self.item_data.get('label')}")

            # Restaurar estilo después de 300ms
            QTimer.singleShot(300, lambda: self.render_button.setStyleSheet(original_style))

        except Exception as e:
            logger.error(f"Error rendering WEB_STATIC: {e}")

            # Restaurar estilo con color de error
            self.render_button.setStyleSheet("""
                QPushButton {
                    background-color: #f44336;
                    color: #ffffff;
                    border: none;
                    border-radius: 3px;
                    font-size: 12pt;
                    padding: 0px;
                }
            """)
            QTimer.singleShot(1000, lambda: self.render_button.setStyleSheet(original_style))

    def render_content(self):
        """Renderizar contenido de WEB_STATIC"""
        # Layout horizontal para icono + título
        title_layout = QHBoxLayout()
        title_layout.setSpacing(8)

        # Icono de app web
        icon_label = QLabel("📱")
        icon_label.setStyleSheet("font-size: 16px;")
        title_layout.addWidget(icon_label)

        # Título
        label = self.get_item_label()
        if label and label != 'Sin título':
            title_label = QLabel(label)
            title_label.setWordWrap(True)
            title_label.setMaximumWidth(680)
            title_label.setStyleSheet("""
                color: #FFFFFF;
                font-size: 14px;
                font-weight: bold;
                font-family: 'Segoe UI', Arial, sans-serif;
                word-break: break-word;
                overflow-wrap: anywhere;
            """)
            title_layout.addWidget(title_label)

        title_layout.addStretch()
        self.content_layout.addLayout(title_layout)

        # Preview del HTML (primeras líneas)
        content = self.get_item_content()
        if content:
            preview_lines = content.split('\n')[:5]  # Primeras 5 líneas
            preview_text = '\n'.join(preview_lines)
            if len(content.split('\n')) > 5:
                preview_text += '\n...'

            preview_label = QLabel(preview_text)
            preview_label.setStyleSheet("""
                color: #90EE90;
                font-family: 'Consolas', 'Courier New', monospace;
                font-size: 12px;
                background-color: #1a1a1a;
                padding: 8px;
                border-radius: 4px;
                white-space: pre-wrap;
            """)
            preview_label.setWordWrap(True)
            preview_label.setMaximumWidth(720)
            preview_label.setTextInteractionFlags(
                Qt.TextInteractionFlag.TextSelectableByMouse
            )
            self.content_layout.addWidget(preview_label)

        # Descripción (si existe)
        description = self.get_item_description()
        if description:
            desc_label = QLabel(description)
            desc_label.setStyleSheet("""
                color: #808080;
                font-size: 12px;
                font-style: italic;
                padding-top: 4px;
                font-family: 'Segoe UI', Arial, sans-serif;
            """)
            desc_label.setWordWrap(True)
            self.content_layout.addWidget(desc_label)

    def apply_styles(self):
        """Aplicar estilos CSS"""
        self.setStyleSheet(FullViewStyles.get_web_static_item_style())
