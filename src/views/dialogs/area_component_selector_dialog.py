"""
Area Component Selector Dialog - Diálogo para seleccionar componentes estructurales

Permite agregar componentes visuales al área: dividers, comments, alerts, notes
"""

from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QPushButton,
                             QLabel, QTextEdit, QComboBox, QLineEdit,
                             QMessageBox, QFrame, QListWidget, QListWidgetItem)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QCursor
import logging

logger = logging.getLogger(__name__)


class AreaComponentSelector(QDialog):
    """Diálogo para seleccionar y crear componentes estructurales para el área"""

    component_created = pyqtSignal(str, dict)  # component_type, component_data

    def __init__(self, parent=None):
        """
        Args:
            parent: Parent widget
        """
        super().__init__(parent)

        self.component_types = {
            'divider': {
                'name': 'Separador',
                'icon': '➖',
                'description': 'Línea separadora visual'
            },
            'comment': {
                'name': 'Comentario',
                'icon': '💬',
                'description': 'Nota o comentario explicativo'
            },
            'alert': {
                'name': 'Alerta',
                'icon': '⚠️',
                'description': 'Mensaje de advertencia o información importante'
            },
            'note': {
                'name': 'Nota',
                'icon': '📝',
                'description': 'Nota informativa destacada'
            }
        }

        self.init_ui()

    def init_ui(self):
        """Inicializa la interfaz"""
        self.setWindowTitle("🧩 Agregar Componente")
        self.setMinimumSize(600, 500)

        # Layout principal
        layout = QVBoxLayout(self)
        layout.setSpacing(15)

        # Header
        header = QLabel("🧩 Agregar Componente Estructural")
        header.setStyleSheet("""
            QLabel {
                font-size: 14pt;
                font-weight: bold;
                color: #9b59b6;
                padding: 10px;
            }
        """)
        layout.addWidget(header)

        # Selector de tipo
        type_label = QLabel("Tipo de Componente:")
        type_label.setStyleSheet("font-weight: bold; color: #ffffff;")
        layout.addWidget(type_label)

        # Lista de tipos de componentes
        self.type_list = QListWidget()
        self.type_list.setMaximumHeight(150)
        for comp_type, data in self.component_types.items():
            item = QListWidgetItem(f"{data['icon']} {data['name']} - {data['description']}")
            item.setData(Qt.ItemDataRole.UserRole, comp_type)
            self.type_list.addItem(item)

        self.type_list.itemClicked.connect(self.on_type_selected)
        layout.addWidget(self.type_list)

        # Frame de configuración del componente
        self.config_frame = QFrame()
        self.config_frame.setFrameStyle(QFrame.Shape.StyledPanel)
        self.config_frame.setStyleSheet("""
            QFrame {
                background-color: #2d2d2d;
                border: 1px solid #9b59b6;
                border-radius: 4px;
                padding: 10px;
            }
        """)
        self.config_frame.setVisible(False)

        config_layout = QVBoxLayout(self.config_frame)

        # Título (para algunos componentes)
        title_label = QLabel("Título (opcional):")
        title_label.setStyleSheet("font-weight: bold; color: #ffffff;")
        config_layout.addWidget(title_label)

        self.title_input = QLineEdit()
        self.title_input.setPlaceholderText("Título del componente...")
        config_layout.addWidget(self.title_input)

        # Contenido (para componentes que lo necesitan)
        content_label = QLabel("Contenido:")
        content_label.setStyleSheet("font-weight: bold; color: #ffffff; margin-top: 10px;")
        config_layout.addWidget(content_label)

        self.content_input = QTextEdit()
        self.content_input.setPlaceholderText("Contenido del componente...")
        self.content_input.setMaximumHeight(150)
        config_layout.addWidget(self.content_input)

        # Estilo/Color (para algunos componentes)
        style_label = QLabel("Estilo:")
        style_label.setStyleSheet("font-weight: bold; color: #ffffff; margin-top: 10px;")
        config_layout.addWidget(style_label)

        self.style_combo = QComboBox()
        config_layout.addWidget(self.style_combo)

        layout.addWidget(self.config_frame)

        # Preview
        preview_label = QLabel("Vista Previa:")
        preview_label.setStyleSheet("font-weight: bold; color: #ffffff; margin-top: 10px;")
        layout.addWidget(preview_label)

        self.preview_frame = QFrame()
        self.preview_frame.setFrameStyle(QFrame.Shape.StyledPanel)
        self.preview_frame.setStyleSheet("""
            QFrame {
                background-color: #2d2d2d;
                border: 1px solid #3d3d3d;
                border-radius: 4px;
                padding: 10px;
                min-height: 60px;
            }
        """)

        preview_layout = QVBoxLayout(self.preview_frame)
        self.preview_label = QLabel("Selecciona un tipo de componente...")
        self.preview_label.setWordWrap(True)
        self.preview_label.setStyleSheet("color: #888888;")
        preview_layout.addWidget(self.preview_label)

        layout.addWidget(self.preview_frame)

        layout.addStretch()

        # Botones
        buttons_layout = QHBoxLayout()

        add_btn = QPushButton("✅ Agregar Componente")
        add_btn.setEnabled(False)
        add_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        add_btn.setStyleSheet(self._get_button_style("#9b59b6"))
        add_btn.clicked.connect(self.on_add_component)
        self.add_btn = add_btn
        buttons_layout.addWidget(add_btn)

        cancel_btn = QPushButton("❌ Cancelar")
        cancel_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        cancel_btn.setStyleSheet(self._get_button_style("#888888"))
        cancel_btn.clicked.connect(self.reject)
        buttons_layout.addWidget(cancel_btn)

        layout.addLayout(buttons_layout)

        # Styling general
        self.setStyleSheet("""
            QDialog {
                background-color: #1e1e1e;
            }
            QLabel {
                color: #ffffff;
            }
            QLineEdit {
                background-color: #2d2d2d;
                color: #ffffff;
                border: 1px solid #3d3d3d;
                padding: 8px;
                border-radius: 4px;
            }
            QTextEdit {
                background-color: #2d2d2d;
                color: #ffffff;
                border: 1px solid #3d3d3d;
                padding: 8px;
                border-radius: 4px;
            }
            QComboBox {
                background-color: #2d2d2d;
                color: #ffffff;
                border: 1px solid #3d3d3d;
                padding: 8px;
                border-radius: 4px;
            }
            QListWidget {
                background-color: #2d2d2d;
                color: #ffffff;
                border: 1px solid #3d3d3d;
                border-radius: 4px;
                padding: 5px;
            }
            QListWidget::item {
                padding: 8px;
                border-radius: 3px;
            }
            QListWidget::item:selected {
                background-color: #9b59b6;
                color: #000000;
            }
            QListWidget::item:hover {
                background-color: #3d3d3d;
            }
        """)

    def _get_button_style(self, color: str) -> str:
        """Retorna estilo para botones"""
        return f"""
            QPushButton {{
                background-color: #2d2d2d;
                color: #ffffff;
                border: 1px solid {color};
                padding: 10px 20px;
                border-radius: 4px;
                font-size: 10pt;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: {color};
                color: #000000;
            }}
            QPushButton:disabled {{
                background-color: #1e1e1e;
                color: #555555;
                border-color: #3d3d3d;
            }}
        """

    def on_type_selected(self, item: QListWidgetItem):
        """Al seleccionar un tipo de componente"""
        comp_type = item.data(Qt.ItemDataRole.UserRole)
        self.selected_type = comp_type

        # Mostrar configuración
        self.config_frame.setVisible(True)
        self.add_btn.setEnabled(True)

        # Configurar campos según el tipo
        if comp_type == 'divider':
            self.title_input.setVisible(True)
            self.content_input.setVisible(False)
            self.style_combo.setVisible(True)
            self.style_combo.clear()
            self.style_combo.addItems(['Línea sólida', 'Línea punteada', 'Línea doble'])

        elif comp_type == 'comment':
            self.title_input.setVisible(False)
            self.content_input.setVisible(True)
            self.style_combo.setVisible(True)
            self.style_combo.clear()
            self.style_combo.addItems(['Normal', 'Destacado', 'Tenue'])

        elif comp_type == 'alert':
            self.title_input.setVisible(True)
            self.content_input.setVisible(True)
            self.style_combo.setVisible(True)
            self.style_combo.clear()
            self.style_combo.addItems(['Info', 'Advertencia', 'Error', 'Éxito'])

        elif comp_type == 'note':
            self.title_input.setVisible(True)
            self.content_input.setVisible(True)
            self.style_combo.setVisible(True)
            self.style_combo.clear()
            self.style_combo.addItems(['Azul', 'Verde', 'Amarillo', 'Naranja', 'Púrpura'])

        # Conectar actualización de preview
        self.title_input.textChanged.connect(self.update_preview)
        self.content_input.textChanged.connect(self.update_preview)
        self.style_combo.currentTextChanged.connect(self.update_preview)

        self.update_preview()

    def update_preview(self):
        """Actualiza la vista previa del componente"""
        if not hasattr(self, 'selected_type'):
            return

        comp_type = self.selected_type
        title = self.title_input.text()
        content = self.content_input.toPlainText()
        style = self.style_combo.currentText()

        preview_html = ""

        if comp_type == 'divider':
            preview_html = f"<b>{title if title else 'Separador'}</b><hr>"

        elif comp_type == 'comment':
            preview_html = f"<span style='color: #888888;'>💬 {content if content else 'Comentario...'}</span>"

        elif comp_type == 'alert':
            color = {'Info': '#3498db', 'Advertencia': '#f39c12', 'Error': '#e74c3c', 'Éxito': '#27ae60'}.get(style, '#3498db')
            preview_html = f"<div style='background-color: {color}; padding: 10px; border-radius: 4px;'>"
            if title:
                preview_html += f"<b>⚠️ {title}</b><br>"
            preview_html += f"{content if content else 'Contenido de la alerta...'}</div>"

        elif comp_type == 'note':
            color = {'Azul': '#3498db', 'Verde': '#27ae60', 'Amarillo': '#f39c12', 'Naranja': '#e67e22', 'Púrpura': '#9b59b6'}.get(style, '#9b59b6')
            preview_html = f"<div style='border-left: 4px solid {color}; padding-left: 10px;'>"
            if title:
                preview_html += f"<b>📝 {title}</b><br>"
            preview_html += f"{content if content else 'Contenido de la nota...'}</div>"

        self.preview_label.setText(preview_html)
        self.preview_label.setStyleSheet("color: #ffffff;")

    def on_add_component(self):
        """Al hacer clic en agregar componente"""
        if not hasattr(self, 'selected_type'):
            QMessageBox.warning(self, "Error", "Selecciona un tipo de componente")
            return

        # Validaciones según el tipo
        if self.selected_type in ['comment', 'alert', 'note']:
            if not self.content_input.toPlainText().strip():
                QMessageBox.warning(self, "Error", "El contenido es requerido para este tipo de componente")
                return

        # Construir datos del componente
        component_data = {
            'title': self.title_input.text().strip() if self.title_input.isVisible() else '',
            'content': self.content_input.toPlainText().strip() if self.content_input.isVisible() else '',
            'style': self.style_combo.currentText() if self.style_combo.isVisible() else ''
        }

        # Emitir señal
        self.component_created.emit(self.selected_type, component_data)

        logger.info(f"Component created: {self.selected_type}")
        self.accept()
