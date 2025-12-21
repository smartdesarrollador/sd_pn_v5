"""
Widget para items de tipo PATH

Muestra items de ruta de archivo/carpeta clickeable.
Para contenido extenso (>1500 chars) muestra botón de colapsar/expandir.

Autor: Widget Sidebar Team
Versión: 2.0
"""

from PyQt6.QtWidgets import QLabel, QHBoxLayout, QPushButton, QSizePolicy
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QCursor
from .base_item_widget import BaseItemWidget
from ...styles.full_view_styles import FullViewStyles
from ..common.copy_button import CopyButton
import subprocess
import os
import platform
import logging

logger = logging.getLogger(__name__)


class PathItemWidget(BaseItemWidget):
    """
    Widget para items de tipo PATH

    Características:
    - Muestra ruta de archivo/carpeta sin límites
    - Click en path abre en explorador de archivos
    - Icono 📁 para carpetas, 📄 para archivos
    - Para contenido extenso (>1500 chars): botón de colapsar/expandir
    - Por defecto: todo el contenido visible (expandido)
    """

    COLLAPSIBLE_LENGTH = 1500  # Límite para mostrar botón de colapso
    COLLAPSED_PREVIEW = 200    # Caracteres a mostrar cuando está colapsado

    def __init__(self, item_data: dict, parent=None):
        """
        Inicializar widget de item de path

        Args:
            item_data: Diccionario con datos del item
            parent: Widget padre
        """
        self.is_expanded = True  # Por defecto expandido
        self.content_label = None
        self.toggle_button = None
        super().__init__(item_data, parent)
        self.apply_styles()

    def _create_action_buttons(self):
        """
        Crear botones de acción específicos para items de PATH

        Botones:
        - Copiar (siempre presente)
        - Abrir en explorador (📁)
        - Abrir archivo (📝) - solo para archivos
        """
        # Botón de copiar
        self.copy_button = CopyButton()
        self.copy_button.copy_clicked.connect(self.copy_to_clipboard)
        self.copy_button.setFixedSize(28, 28)
        self.copy_button.setToolTip("Copiar ruta")
        self.buttons_layout.addWidget(self.copy_button)

        # Botón abrir en explorador
        self.open_explorer_button = QPushButton("📁")
        self.open_explorer_button.setFixedSize(28, 28)
        self.open_explorer_button.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.open_explorer_button.setStyleSheet("""
            QPushButton {
                background-color: #2d7d2d;
                color: #ffffff;
                border: none;
                border-radius: 3px;
                font-size: 12pt;
                padding: 0px;
            }
            QPushButton:hover {
                background-color: #236123;
            }
            QPushButton:pressed {
                background-color: #1a4a1a;
            }
        """)
        self.open_explorer_button.setToolTip("Abrir en explorador")
        self.open_explorer_button.clicked.connect(self._open_in_explorer)
        self.buttons_layout.addWidget(self.open_explorer_button)

        # Botón abrir archivo (solo si es archivo)
        path_content = self.item_data.get('content', '')
        if path_content and os.path.exists(path_content) and os.path.isfile(path_content):
            self.open_file_button = QPushButton("📝")
            self.open_file_button.setFixedSize(28, 28)
            self.open_file_button.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
            self.open_file_button.setStyleSheet("""
                QPushButton {
                    background-color: #cc7a00;
                    color: #ffffff;
                    border: none;
                    border-radius: 3px;
                    font-size: 12pt;
                    padding: 0px;
                }
                QPushButton:hover {
                    background-color: #9e5e00;
                }
                QPushButton:pressed {
                    background-color: #784500;
                }
            """)
            self.open_file_button.setToolTip("Abrir archivo")
            self.open_file_button.clicked.connect(self._open_file)
            self.buttons_layout.addWidget(self.open_file_button)

    def _open_in_explorer(self):
        """Abrir en explorador de archivos"""
        path_content = self.item_data.get('content', '')
        if not path_content:
            return

        try:
            system = platform.system()

            if system == 'Windows':
                if os.path.exists(path_content):
                    subprocess.run(['explorer', '/select,', os.path.abspath(path_content)])
                else:
                    parent = os.path.dirname(path_content)
                    if os.path.exists(parent):
                        subprocess.run(['explorer', os.path.abspath(parent)])
            elif system == 'Darwin':  # macOS
                if os.path.exists(path_content):
                    subprocess.run(['open', '-R', os.path.abspath(path_content)])
            else:  # Linux
                if os.path.exists(path_content):
                    if os.path.isfile(path_content):
                        subprocess.run(['xdg-open', os.path.dirname(os.path.abspath(path_content))])
                    else:
                        subprocess.run(['xdg-open', os.path.abspath(path_content)])

            logger.info(f"Opened path in explorer: {path_content}")

            # Visual feedback
            original_style = self.open_explorer_button.styleSheet()
            self.open_explorer_button.setStyleSheet("""
                QPushButton {
                    background-color: #00ff00;
                    color: #ffffff;
                    border: none;
                    border-radius: 3px;
                    font-size: 12pt;
                    padding: 0px;
                }
            """)
            QTimer.singleShot(300, lambda: self.open_explorer_button.setStyleSheet(original_style))

        except Exception as e:
            logger.error(f"Error opening path in explorer: {e}")

    def _open_file(self):
        """Abrir archivo con aplicación predeterminada"""
        path_content = self.item_data.get('content', '')
        if not path_content or not os.path.exists(path_content) or not os.path.isfile(path_content):
            return

        try:
            system = platform.system()

            if system == 'Windows':
                os.startfile(os.path.abspath(path_content))
            elif system == 'Darwin':  # macOS
                subprocess.run(['open', os.path.abspath(path_content)])
            else:  # Linux
                subprocess.run(['xdg-open', os.path.abspath(path_content)])

            logger.info(f"Opened file: {path_content}")

            # Visual feedback
            original_style = self.open_file_button.styleSheet()
            self.open_file_button.setStyleSheet("""
                QPushButton {
                    background-color: #00ff00;
                    color: #ffffff;
                    border: none;
                    border-radius: 3px;
                    font-size: 12pt;
                    padding: 0px;
                }
            """)
            QTimer.singleShot(300, lambda: self.open_file_button.setStyleSheet(original_style))

        except Exception as e:
            logger.error(f"Error opening file: {e}")

    def render_content(self):
        """Renderizar contenido de PATH sin límites ni scroll"""
        # Layout horizontal para icono + título
        title_layout = QHBoxLayout()
        title_layout.setSpacing(8)

        # Determinar icono según tipo de path
        path_content = self.get_item_content()
        icon = "📁" if os.path.isdir(path_content) else "📄"

        icon_label = QLabel(icon)
        icon_label.setStyleSheet("font-size: 16px;")
        title_layout.addWidget(icon_label)

        # Título
        label = self.get_item_label()
        if label and label != 'Sin título':
            title_label = QLabel(label)
            title_label.setWordWrap(True)
            title_label.setMaximumWidth(680)  # Menor porque hay icono
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

        # Path clickeable
        if path_content:
            self.content_label = QLabel()
            self.content_label.setObjectName("path_text")
            self.content_label.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
            self.content_label.setTextInteractionFlags(
                Qt.TextInteractionFlag.TextSelectableByMouse
            )
            self.content_label.setWordWrap(True)  # IMPORTANTE: ajustar al ancho
            self.content_label.setSizePolicy(
                QSizePolicy.Policy.Expanding,
                QSizePolicy.Policy.Preferred
            )
            self.content_label.mousePressEvent = lambda event: self.open_path(path_content)
            self.content_label.setToolTip("Click para abrir en explorador")
            self.content_label.setStyleSheet("""
                color: #FFA500;
                font-family: 'Consolas', 'Courier New', monospace;
                font-size: 12px;
                word-wrap: break-word;
                word-break: break-word;
                overflow-wrap: anywhere;
            """)

            # Si el contenido es largo, mostrar todo por defecto (expandido)
            if len(path_content) > self.COLLAPSIBLE_LENGTH:
                self.content_label.setText(path_content)
                self.content_layout.addWidget(self.content_label)

                # Agregar botón de colapsar/expandir
                self.toggle_button = QPushButton("▲ Colapsar")
                self.toggle_button.setCursor(Qt.CursorShape.PointingHandCursor)
                self.toggle_button.clicked.connect(self.toggle_content)
                self.toggle_button.setStyleSheet("""
                    QPushButton {
                        background-color: transparent;
                        border: 1px solid #8B4513;
                        border-radius: 4px;
                        padding: 6px 12px;
                        color: #FFA500;
                        font-size: 12px;
                        font-weight: bold;
                        margin-top: 8px;
                    }
                    QPushButton:hover {
                        background-color: #2A2A2A;
                        border-color: #FFA500;
                    }
                """)
                self.content_layout.addWidget(self.toggle_button)
            else:
                # Contenido corto: mostrar todo sin botón
                self.content_label.setText(path_content)
                self.content_layout.addWidget(self.content_label)

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

    def toggle_content(self):
        """Alternar entre contenido colapsado y expandido"""
        content = self.get_item_content()

        if self.is_expanded:
            # Colapsar: mostrar solo preview
            preview = content[:self.COLLAPSED_PREVIEW] + "..."
            self.content_label.setText(preview)
            self.toggle_button.setText("▼ Expandir")
            self.is_expanded = False
        else:
            # Expandir: mostrar todo
            self.content_label.setText(content)
            self.toggle_button.setText("▲ Colapsar")
            self.is_expanded = True

    def open_path(self, path: str):
        """
        Abrir path en explorador de archivos

        Args:
            path: Ruta a abrir
        """
        try:
            if os.path.exists(path):
                # Windows: abrir en explorador con selección
                subprocess.Popen(f'explorer /select,"{path}"')
                print(f"✓ Path abierto: {path}")
            else:
                print(f"✗ Path no existe: {path}")
        except Exception as e:
            print(f"✗ Error al abrir path: {e}")

    def apply_styles(self):
        """Aplicar estilos CSS"""
        self.setStyleSheet(FullViewStyles.get_path_item_style())
