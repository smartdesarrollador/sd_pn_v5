"""
Widget para items de tipo CODE

Muestra items de código sin límites.
Para contenido extenso (>1500 chars) muestra botón de colapsar/expandir.

Autor: Widget Sidebar Team
Versión: 2.0
"""

from PyQt6.QtWidgets import QLabel, QPushButton, QSizePolicy
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QCursor
from .base_item_widget import BaseItemWidget
from ...styles.full_view_styles import FullViewStyles
from ..common.copy_button import CopyButton
import subprocess
import platform
import logging

logger = logging.getLogger(__name__)


class CodeItemWidget(BaseItemWidget):
    """
    Widget para items de tipo CODE

    Características:
    - Muestra código sin límites
    - Font monospace (Consolas, Courier New)
    - Para contenido extenso (>1500 chars): botón de colapsar/expandir
    - Por defecto: todo el contenido visible (expandido)
    """

    COLLAPSIBLE_LENGTH = 1500  # Límite para mostrar botón de colapso
    COLLAPSED_PREVIEW = 200    # Caracteres a mostrar cuando está colapsado

    def __init__(self, item_data: dict, parent=None):
        """
        Inicializar widget de item de código

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
        Crear botones de acción específicos para items de CODE

        Botones:
        - Ejecutar comando (⚡)
        - Copiar (siempre presente)
        """
        # Botón ejecutar comando
        self.execute_button = QPushButton("⚡")
        self.execute_button.setFixedSize(28, 28)
        self.execute_button.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.execute_button.setStyleSheet("""
            QPushButton {
                background-color: #cc7a00;
                color: #000000;
                border: none;
                border-radius: 3px;
                font-size: 12pt;
                padding: 0px;
            }
            QPushButton:hover {
                background-color: #9e5e00;
                color: #ffffff;
            }
            QPushButton:pressed {
                background-color: #784500;
            }
        """)
        self.execute_button.setToolTip("Ejecutar comando")
        self.execute_button.clicked.connect(self._execute_command)
        self.buttons_layout.addWidget(self.execute_button)

        # Botón de copiar
        self.copy_button = CopyButton()
        self.copy_button.copy_clicked.connect(self.copy_to_clipboard)
        self.copy_button.setFixedSize(28, 28)
        self.copy_button.setToolTip("Copiar código")
        self.buttons_layout.addWidget(self.copy_button)

    def _execute_command(self):
        """Ejecutar comando de código"""
        command = self.item_data.get('content', '')
        if not command:
            return

        try:
            # Visual feedback - cambiar botón a amarillo mientras ejecuta
            original_style = self.execute_button.styleSheet()
            self.execute_button.setStyleSheet("""
                QPushButton {
                    background-color: #ffff00;
                    color: #000000;
                    border: none;
                    border-radius: 3px;
                    font-size: 12pt;
                    padding: 0px;
                }
            """)
            self.execute_button.setText("⏳")

            # Ejecutar comando
            system = platform.system()
            working_dir = self.item_data.get('working_dir', None)

            if system == 'Windows':
                result = subprocess.run(
                    command,
                    shell=True,
                    capture_output=True,
                    text=True,
                    timeout=30,
                    cwd=working_dir
                )
            else:
                result = subprocess.run(
                    command,
                    shell=True,
                    capture_output=True,
                    text=True,
                    timeout=30,
                    executable='/bin/bash',
                    cwd=working_dir
                )

            # Restaurar botón
            self.execute_button.setText("⚡")
            if result.returncode == 0:
                # Verde si éxito
                self.execute_button.setStyleSheet("""
                    QPushButton {
                        background-color: #00ff00;
                        color: #000000;
                        border: none;
                        border-radius: 3px;
                        font-size: 12pt;
                        padding: 0px;
                    }
                """)
                logger.info(f"Command executed successfully: {command}")
            else:
                # Rojo si error
                self.execute_button.setStyleSheet("""
                    QPushButton {
                        background-color: #ff0000;
                        color: #ffffff;
                        border: none;
                        border-radius: 3px;
                        font-size: 12pt;
                        padding: 0px;
                    }
                """)
                logger.error(f"Command failed: {command}")

            # Restaurar estilo original después de 1 segundo
            QTimer.singleShot(1000, lambda: self.execute_button.setStyleSheet(original_style))

            # Mostrar dialog con resultado
            from src.views.command_output_dialog import CommandOutputDialog
            dialog = CommandOutputDialog(
                command=command,
                output=result.stdout,
                error=result.stderr,
                return_code=result.returncode,
                parent=self.window()
            )
            dialog.exec()

        except subprocess.TimeoutExpired:
            logger.error(f"Command timeout: {command}")
            self.execute_button.setText("⚡")
            self.execute_button.setStyleSheet("""
                QPushButton {
                    background-color: #ff0000;
                    color: #ffffff;
                    border: none;
                    border-radius: 3px;
                    font-size: 12pt;
                    padding: 0px;
                }
            """)
            QTimer.singleShot(1000, lambda: self.execute_button.setStyleSheet(original_style))

        except Exception as e:
            logger.error(f"Error executing command: {e}")
            self.execute_button.setText("⚡")
            self.execute_button.setStyleSheet("""
                QPushButton {
                    background-color: #ff0000;
                    color: #ffffff;
                    border: none;
                    border-radius: 3px;
                    font-size: 12pt;
                    padding: 0px;
                }
            """)
            QTimer.singleShot(1000, lambda: self.execute_button.setStyleSheet(original_style))

    def render_content(self):
        """Renderizar contenido de código sin límites ni scroll"""
        # Título (si existe)
        label = self.get_item_label()
        if label and label != 'Sin título':
            title_label = QLabel(f"$ {label}")
            title_label.setWordWrap(True)
            title_label.setMaximumWidth(720)
            title_label.setStyleSheet("""
                color: #7CFC00;
                font-size: 13px;
                font-weight: bold;
                font-family: 'Consolas', 'Courier New', monospace;
                padding-bottom: 6px;
                word-break: break-word;
                overflow-wrap: anywhere;
            """)
            self.content_layout.addWidget(title_label)

        # Contenido de código
        content = self.get_item_content()
        if content:
            # Crear label para el código (sin límites, 100% responsive)
            self.content_label = QLabel()
            self.content_label.setObjectName("code_content")
            self.content_label.setWordWrap(True)  # IMPORTANTE: ajustar al ancho
            self.content_label.setMaximumWidth(720)  # Limitar ancho para evitar overflow
            self.content_label.setTextInteractionFlags(
                Qt.TextInteractionFlag.TextSelectableByMouse
            )
            self.content_label.setSizePolicy(
                QSizePolicy.Policy.Expanding,
                QSizePolicy.Policy.Preferred
            )
            self.content_label.setStyleSheet("""
                color: #7CFC00;
                font-family: 'Consolas', 'Courier New', monospace;
                font-size: 12px;
                background-color: transparent;
                white-space: pre-wrap;
                word-wrap: break-word;
                word-break: break-word;
                overflow-wrap: anywhere;
            """)

            # Si el contenido es largo, mostrar todo por defecto (expandido)
            if len(content) > self.COLLAPSIBLE_LENGTH:
                self.content_label.setText(content)
                self.content_layout.addWidget(self.content_label)

                # Agregar botón de colapsar/expandir
                self.toggle_button = QPushButton("▲ Colapsar")
                self.toggle_button.setCursor(Qt.CursorShape.PointingHandCursor)
                self.toggle_button.clicked.connect(self.toggle_content)
                self.toggle_button.setStyleSheet("""
                    QPushButton {
                        background-color: transparent;
                        border: 1px solid #2D4A2B;
                        border-radius: 4px;
                        padding: 6px 12px;
                        color: #7CFC00;
                        font-size: 12px;
                        font-weight: bold;
                        margin-top: 8px;
                    }
                    QPushButton:hover {
                        background-color: #141920;
                        border-color: #7CFC00;
                    }
                """)
                self.content_layout.addWidget(self.toggle_button)
            else:
                # Contenido corto: mostrar todo sin botón
                self.content_label.setText(content)
                self.content_layout.addWidget(self.content_label)

    def toggle_content(self):
        """Alternar entre contenido colapsado y expandido"""
        content = self.get_item_content()

        if self.is_expanded:
            # Colapsar: mostrar solo preview
            preview = content[:self.COLLAPSED_PREVIEW] + "\n..."
            self.content_label.setText(preview)
            self.toggle_button.setText("▼ Expandir")
            self.is_expanded = False
        else:
            # Expandir: mostrar todo
            self.content_label.setText(content)
            self.toggle_button.setText("▲ Colapsar")
            self.is_expanded = True

    def apply_styles(self):
        """Aplicar estilos CSS"""
        self.setStyleSheet(FullViewStyles.get_code_item_style())
