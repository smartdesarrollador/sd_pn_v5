"""
Area Tag Manager Dialog - Diálogo completo de gestión de tags

Diálogo para administrar tags: crear, editar, eliminar y ver estadísticas.
"""

from typing import Optional
from PyQt6.QtWidgets import (
    QDialog, QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QTableWidget, QTableWidgetItem, QHeaderView,
    QLineEdit, QLabel, QColorDialog, QTextEdit,
    QMessageBox, QDialogButtonBox
)
from PyQt6.QtCore import pyqtSignal, Qt
from PyQt6.QtGui import QFont, QColor, QCursor

from src.core.area_element_tag_manager import AreaElementTagManager
from src.models.area_element_tag import AreaElementTag


class AreaTagEditorDialog(QDialog):
    """Diálogo para crear/editar un tag"""

    def __init__(self, tag_manager: AreaElementTagManager, tag: Optional[AreaElementTag] = None, parent=None):
        """
        Inicializa el diálogo

        Args:
            tag_manager: Manager de tags
            tag: Tag a editar (None para crear nuevo)
            parent: Widget padre
        """
        super().__init__(parent)
        self.tag_manager = tag_manager
        self.tag = tag
        self.selected_color = tag.color if tag else "#9b59b6"
        self._setup_ui()

    def _setup_ui(self):
        """Configura la UI del diálogo"""
        self.setWindowTitle("Editar Tag" if self.tag else "Crear Tag")
        self.setMinimumWidth(400)

        layout = QVBoxLayout(self)
        layout.setSpacing(12)

        # Nombre
        name_layout = QHBoxLayout()
        name_label = QLabel("Nombre:")
        name_label.setFont(QFont("Segoe UI", 10, QFont.Weight.Bold))
        name_layout.addWidget(name_label)

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Nombre del tag (max 50 caracteres)")
        self.name_input.setMaxLength(50)
        if self.tag:
            self.name_input.setText(self.tag.name)
        name_layout.addWidget(self.name_input)
        layout.addLayout(name_layout)

        # Color
        color_layout = QHBoxLayout()
        color_label = QLabel("Color:")
        color_label.setFont(QFont("Segoe UI", 10, QFont.Weight.Bold))
        color_layout.addWidget(color_label)

        self.color_btn = QPushButton("Seleccionar Color")
        self.color_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.color_btn.clicked.connect(self._select_color)
        self._update_color_button()
        color_layout.addWidget(self.color_btn)
        layout.addLayout(color_layout)

        # Descripción
        desc_label = QLabel("Descripción (opcional):")
        desc_label.setFont(QFont("Segoe UI", 10, QFont.Weight.Bold))
        layout.addWidget(desc_label)

        self.description_input = QTextEdit()
        self.description_input.setMaximumHeight(80)
        self.description_input.setPlaceholderText("Descripción del tag...")
        if self.tag:
            self.description_input.setPlainText(self.tag.description)
        layout.addWidget(self.description_input)

        # Botones
        button_box = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Save | QDialogButtonBox.StandardButton.Cancel
        )
        button_box.accepted.connect(self._save)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)

        self._apply_styles()

    def _apply_styles(self):
        """Aplica estilos CSS"""
        self.setStyleSheet("""
            QDialog {
                background-color: #2c3e50;
            }
            QLabel {
                color: #ecf0f1;
            }
            QLineEdit, QTextEdit {
                padding: 8px;
                border: 2px solid #34495e;
                border-radius: 6px;
                background-color: #34495e;
                color: #ecf0f1;
                font-size: 10pt;
            }
            QLineEdit:focus, QTextEdit:focus {
                border: 2px solid #9b59b6;
            }
            QPushButton {
                padding: 8px 16px;
                background-color: #9b59b6;
                color: white;
                border: none;
                border-radius: 6px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #bb79d6;
            }
        """)

    def _select_color(self):
        """Abre diálogo de selección de color"""
        color = QColorDialog.getColor(QColor(self.selected_color), self)
        if color.isValid():
            self.selected_color = color.name()
            self._update_color_button()

    def _update_color_button(self):
        """Actualiza el botón de color con el color seleccionado"""
        self.color_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {self.selected_color};
                color: white;
                padding: 8px 16px;
                border: none;
                border-radius: 6px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                border: 2px solid white;
            }}
        """)

    def _save(self):
        """Guarda el tag"""
        name = self.name_input.text().strip()
        description = self.description_input.toPlainText().strip()

        # Validar nombre
        is_valid, msg = self.tag_manager.validate_tag_name(name)
        if not is_valid:
            QMessageBox.warning(self, "Error", msg)
            return

        # Validar color
        if not self.tag_manager.validate_color(self.selected_color):
            QMessageBox.warning(self, "Error", "Color inválido")
            return

        # Crear o actualizar
        if self.tag:
            # Actualizar
            success = self.tag_manager.update_tag(
                self.tag.id,
                name=name,
                color=self.selected_color,
                description=description
            )
            if not success:
                QMessageBox.warning(self, "Error", "No se pudo actualizar el tag")
                return
        else:
            # Crear
            tag = self.tag_manager.create_tag(name, self.selected_color, description)
            if not tag:
                QMessageBox.warning(self, "Error", "No se pudo crear el tag")
                return

        self.accept()


class AreaTagManagerDialog(QDialog):
    """
    Diálogo completo de gestión de tags

    Permite crear, editar, eliminar tags y ver estadísticas de uso.
    """

    # Señales
    tag_created = pyqtSignal(int)   # tag_id
    tag_updated = pyqtSignal(int)   # tag_id
    tag_deleted = pyqtSignal(int)   # tag_id

    def __init__(self, tag_manager: AreaElementTagManager, parent=None):
        """
        Inicializa el diálogo

        Args:
            tag_manager: Manager de tags
            parent: Widget padre
        """
        super().__init__(parent)
        self.tag_manager = tag_manager
        self._setup_ui()
        self._connect_signals()
        self.refresh_tag_list()

    def _setup_ui(self):
        """Configura la UI del diálogo"""
        self.setWindowTitle("🏷️ Gestor de Tags del Área")
        self.setMinimumSize(700, 500)

        layout = QVBoxLayout(self)
        layout.setSpacing(12)

        # Header
        header = QLabel("🏷️ Gestor de Tags del Área")
        header.setStyleSheet("""
            QLabel {
                font-size: 14pt;
                font-weight: bold;
                color: #9b59b6;
                padding: 10px;
            }
        """)
        layout.addWidget(header)

        # Botones de acción
        buttons_layout = QHBoxLayout()

        self.create_btn = QPushButton("➕ Crear Tag")
        self.create_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.create_btn.clicked.connect(self.show_create_dialog)
        buttons_layout.addWidget(self.create_btn)

        self.edit_btn = QPushButton("✏️ Editar")
        self.edit_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.edit_btn.clicked.connect(self._edit_selected)
        self.edit_btn.setEnabled(False)
        buttons_layout.addWidget(self.edit_btn)

        self.delete_btn = QPushButton("🗑️ Eliminar")
        self.delete_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.delete_btn.clicked.connect(self._delete_selected)
        self.delete_btn.setEnabled(False)
        buttons_layout.addWidget(self.delete_btn)

        buttons_layout.addStretch()

        self.refresh_btn = QPushButton("🔄 Actualizar")
        self.refresh_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.refresh_btn.clicked.connect(self.refresh_tag_list)
        buttons_layout.addWidget(self.refresh_btn)

        layout.addLayout(buttons_layout)

        # Tabla de tags
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["Nombre", "Color", "Descripción", "Usos"])
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.table.itemSelectionChanged.connect(self._on_selection_changed)
        self.table.itemDoubleClicked.connect(lambda: self._edit_selected())

        # Configurar columnas
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Fixed)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.Fixed)
        self.table.setColumnWidth(1, 100)
        self.table.setColumnWidth(3, 80)

        layout.addWidget(self.table)

        # Botón cerrar
        close_layout = QHBoxLayout()
        close_layout.addStretch()

        close_btn = QPushButton("✅ Cerrar")
        close_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        close_btn.clicked.connect(self.accept)
        close_layout.addWidget(close_btn)

        layout.addLayout(close_layout)

        self._apply_styles()

    def _apply_styles(self):
        """Aplica estilos CSS"""
        self.setStyleSheet("""
            QDialog {
                background-color: #1e1e1e;
            }
            QLabel {
                color: #ffffff;
            }
            QPushButton {
                padding: 8px 16px;
                background-color: #9b59b6;
                color: white;
                border: none;
                border-radius: 6px;
                font-weight: bold;
                font-size: 10pt;
            }
            QPushButton:hover {
                background-color: #bb79d6;
            }
            QPushButton:disabled {
                background-color: #7f8c8d;
            }
            QTableWidget {
                background-color: #34495e;
                color: #ecf0f1;
                border: 1px solid #2c3e50;
                border-radius: 6px;
                font-size: 10pt;
            }
            QTableWidget::item {
                padding: 8px;
            }
            QTableWidget::item:selected {
                background-color: #9b59b6;
            }
            QHeaderView::section {
                background-color: #2c3e50;
                color: #ecf0f1;
                padding: 8px;
                border: none;
                font-weight: bold;
            }
        """)

    def _connect_signals(self):
        """Conecta señales del manager"""
        self.tag_manager.tag_created.connect(lambda _: self.refresh_tag_list())
        self.tag_manager.tag_updated.connect(lambda _: self.refresh_tag_list())
        self.tag_manager.tag_deleted.connect(lambda _: self.refresh_tag_list())

    def refresh_tag_list(self):
        """Actualiza la lista de tags"""
        self.table.setRowCount(0)

        tags = self.tag_manager.get_all_tags(refresh=True)

        for tag in tags:
            row = self.table.rowCount()
            self.table.insertRow(row)

            # Nombre
            name_item = QTableWidgetItem(tag.name)
            name_item.setData(Qt.ItemDataRole.UserRole, tag.id)
            self.table.setItem(row, 0, name_item)

            # Color (chip visual)
            color_item = QTableWidgetItem("●")
            color_item.setForeground(QColor(tag.color))
            color_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            color_item.setFont(QFont("Segoe UI", 24))
            self.table.setItem(row, 1, color_item)

            # Descripción
            desc_item = QTableWidgetItem(tag.description[:50] + "..." if len(tag.description) > 50 else tag.description)
            self.table.setItem(row, 2, desc_item)

            # Usos
            usage_count = self.tag_manager.get_tag_usage_count(tag.id)
            usage_item = QTableWidgetItem(str(usage_count))
            usage_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.table.setItem(row, 3, usage_item)

    def _on_selection_changed(self):
        """Maneja cambio de selección en tabla"""
        has_selection = len(self.table.selectedItems()) > 0
        self.edit_btn.setEnabled(has_selection)
        self.delete_btn.setEnabled(has_selection)

    def show_create_dialog(self):
        """Muestra diálogo para crear tag"""
        dialog = AreaTagEditorDialog(self.tag_manager, parent=self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.tag_created.emit(0)  # ID será asignado por el manager

    def _edit_selected(self):
        """Edita el tag seleccionado"""
        selected_items = self.table.selectedItems()
        if not selected_items:
            return

        tag_id = selected_items[0].data(Qt.ItemDataRole.UserRole)
        tag = self.tag_manager.get_tag(tag_id)

        if not tag:
            return

        dialog = AreaTagEditorDialog(self.tag_manager, tag, parent=self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.tag_updated.emit(tag_id)

    def _delete_selected(self):
        """Elimina el tag seleccionado"""
        selected_items = self.table.selectedItems()
        if not selected_items:
            return

        tag_id = selected_items[0].data(Qt.ItemDataRole.UserRole)
        tag = self.tag_manager.get_tag(tag_id)

        if not tag:
            return

        # Confirmar
        reply = QMessageBox.question(
            self,
            "Confirmar eliminación",
            f"¿Eliminar el tag '{tag.name}'?\n\nEsto lo removerá de todos los elementos del área.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            success = self.tag_manager.delete_tag(tag_id)
            if success:
                self.tag_deleted.emit(tag_id)
            else:
                QMessageBox.warning(self, "Error", "No se pudo eliminar el tag")

    def show_edit_dialog(self, tag_id: int):
        """
        Muestra diálogo para editar un tag específico

        Args:
            tag_id: ID del tag a editar
        """
        tag = self.tag_manager.get_tag(tag_id)
        if tag:
            dialog = AreaTagEditorDialog(self.tag_manager, tag, parent=self)
            if dialog.exec() == QDialog.DialogCode.Accepted:
                self.tag_updated.emit(tag_id)
