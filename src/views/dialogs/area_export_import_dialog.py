"""
Area Export Import Dialog - Diálogo combinado para exportar e importar áreas
"""

from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QPushButton,
                             QLabel, QFileDialog, QMessageBox, QTextEdit,
                             QGroupBox, QCheckBox, QRadioButton, QButtonGroup,
                             QTabWidget, QWidget)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QCursor
import logging
from pathlib import Path
import json

logger = logging.getLogger(__name__)


class AreaExportImportDialog(QDialog):
    """Diálogo combinado para exportar e importar áreas"""

    export_completed = pyqtSignal(str)  # file_path
    import_completed = pyqtSignal(int)  # area_id

    def __init__(self, export_manager, area_data: dict = None, parent=None):
        """
        Args:
            export_manager: Instancia de AreaExportManager
            area_data: Datos del área (para exportar, opcional)
            parent: Parent widget
        """
        super().__init__(parent)

        self.export_manager = export_manager
        self.area_data = area_data
        self.selected_export_path = None
        self.selected_import_file = None
        self.import_file_data = None

        self.init_ui()

        # Si hay area_data, mostrar tab de exportación
        if area_data:
            self.tabs.setCurrentIndex(0)
            self.load_export_summary()

    def init_ui(self):
        """Inicializa la interfaz"""
        self.setWindowTitle("📦 Exportar/Importar Área")
        self.setMinimumSize(600, 500)

        layout = QVBoxLayout(self)
        layout.setSpacing(15)

        # Header
        header = QLabel("📦 Exportar/Importar Área")
        header.setStyleSheet("""
            QLabel {
                font-size: 14pt;
                font-weight: bold;
                color: #9b59b6;
                padding: 10px;
            }
        """)
        layout.addWidget(header)

        # Tabs
        self.tabs = QTabWidget()

        # Tab de exportación
        export_tab = self._create_export_tab()
        self.tabs.addTab(export_tab, "📤 Exportar")

        # Tab de importación
        import_tab = self._create_import_tab()
        self.tabs.addTab(import_tab, "📥 Importar")

        layout.addWidget(self.tabs)

        # Botón cerrar
        close_layout = QHBoxLayout()
        close_layout.addStretch()

        close_btn = QPushButton("❌ Cerrar")
        close_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        close_btn.setStyleSheet(self._get_button_style("#888888"))
        close_btn.clicked.connect(self.reject)
        close_layout.addWidget(close_btn)

        layout.addLayout(close_layout)

        # Styling
        self.setStyleSheet("""
            QDialog {
                background-color: #1e1e1e;
            }
            QLabel {
                color: #ffffff;
            }
            QGroupBox {
                color: #9b59b6;
                font-weight: bold;
                border: 1px solid #3d3d3d;
                border-radius: 4px;
                margin-top: 10px;
                padding-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px;
            }
            QTextEdit {
                background-color: #2d2d2d;
                color: #ffffff;
                border: 1px solid #3d3d3d;
                border-radius: 4px;
                padding: 8px;
            }
            QCheckBox, QRadioButton {
                color: #ffffff;
            }
            QTabWidget::pane {
                border: 1px solid #3d3d3d;
                background-color: #1e1e1e;
            }
            QTabBar::tab {
                background-color: #2d2d2d;
                color: #ffffff;
                padding: 10px 20px;
                border: 1px solid #3d3d3d;
            }
            QTabBar::tab:selected {
                background-color: #9b59b6;
                color: #000000;
            }
        """)

    def _create_export_tab(self) -> QWidget:
        """Crea la pestaña de exportación"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setSpacing(15)

        # Resumen
        summary_group = QGroupBox("📊 Resumen del Área")
        summary_layout = QVBoxLayout(summary_group)

        self.summary_text = QTextEdit()
        self.summary_text.setReadOnly(True)
        self.summary_text.setMaximumHeight(150)
        summary_layout.addWidget(self.summary_text)

        layout.addWidget(summary_group)

        # Opciones de exportación
        options_group = QGroupBox("⚙️ Opciones de Exportación")
        options_layout = QVBoxLayout(options_group)

        self.include_metadata_check = QCheckBox("Incluir metadata de elementos")
        self.include_metadata_check.setChecked(True)
        self.include_metadata_check.setToolTip("Incluye información detallada de cada elemento (recomendado)")
        options_layout.addWidget(self.include_metadata_check)

        layout.addWidget(options_group)

        # Ruta de destino
        path_layout = QHBoxLayout()

        path_label = QLabel("📁 Archivo de destino:")
        path_label.setStyleSheet("font-weight: bold; color: #ffffff;")
        path_layout.addWidget(path_label)

        self.export_path_display = QLabel("(No seleccionado)")
        self.export_path_display.setStyleSheet("color: #888888;")
        path_layout.addWidget(self.export_path_display, 1)

        browse_export_btn = QPushButton("📂 Examinar...")
        browse_export_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        browse_export_btn.clicked.connect(self.on_browse_export)
        path_layout.addWidget(browse_export_btn)

        layout.addLayout(path_layout)

        layout.addStretch()

        # Botón exportar
        export_btn = QPushButton("📤 Exportar Área")
        export_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        export_btn.setStyleSheet(self._get_button_style("#9b59b6"))
        export_btn.clicked.connect(self.on_export)
        layout.addWidget(export_btn)

        return tab

    def _create_import_tab(self) -> QWidget:
        """Crea la pestaña de importación"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setSpacing(15)

        # Selección de archivo
        file_group = QGroupBox("📁 Archivo a Importar")
        file_layout = QVBoxLayout(file_group)

        file_row = QHBoxLayout()

        self.import_file_display = QLabel("(No seleccionado)")
        self.import_file_display.setStyleSheet("color: #888888;")
        file_row.addWidget(self.import_file_display, 1)

        browse_import_btn = QPushButton("📂 Examinar...")
        browse_import_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        browse_import_btn.clicked.connect(self.on_browse_import)
        file_row.addWidget(browse_import_btn)

        file_layout.addLayout(file_row)

        layout.addWidget(file_group)

        # Vista previa
        preview_group = QGroupBox("👁️ Vista Previa del Archivo")
        preview_layout = QVBoxLayout(preview_group)

        self.import_preview_text = QTextEdit()
        self.import_preview_text.setReadOnly(True)
        self.import_preview_text.setMaximumHeight(150)
        self.import_preview_text.setPlaceholderText("Selecciona un archivo para ver su contenido...")
        preview_layout.addWidget(self.import_preview_text)

        layout.addWidget(preview_group)

        # Opciones de importación
        options_group = QGroupBox("⚙️ Opciones de Importación")
        options_layout = QVBoxLayout(options_group)

        self.mode_group = QButtonGroup(self)

        self.new_area_radio = QRadioButton("Crear como nueva área")
        self.new_area_radio.setChecked(True)
        self.new_area_radio.setToolTip("Crea una nueva área con los datos importados")
        self.mode_group.addButton(self.new_area_radio, 0)
        options_layout.addWidget(self.new_area_radio)

        info_label = QLabel("ℹ️ Nota: Solo se importarán relaciones de elementos que existan en la base de datos")
        info_label.setStyleSheet("color: #888888; font-size: 9pt; font-style: italic;")
        info_label.setWordWrap(True)
        options_layout.addWidget(info_label)

        layout.addWidget(options_group)

        layout.addStretch()

        # Botón importar
        import_btn = QPushButton("📥 Importar Área")
        import_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        import_btn.setStyleSheet(self._get_button_style("#9b59b6"))
        import_btn.clicked.connect(self.on_import)
        layout.addWidget(import_btn)

        return tab

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
        """

    def load_export_summary(self):
        """Carga el resumen del área para exportación"""
        if not self.area_data:
            self.summary_text.setPlainText("No hay área seleccionada para exportar")
            return

        try:
            summary = self.export_manager.get_export_summary(self.area_data['id'])

            if not summary:
                self.summary_text.setPlainText("Error obteniendo resumen del área")
                return

            # Construir texto de resumen
            text = f"Área: {summary['area_name']}\n\n"
            text += f"Total de elementos: {summary['total_relations']}\n"

            if summary['relations_by_type']:
                text += "\nElementos por tipo:\n"
                for entity_type, count in summary['relations_by_type'].items():
                    text += f"  • {entity_type}: {count}\n"

            text += f"\nComponentes estructurales: {summary['total_components']}\n"

            if summary['components_by_type']:
                text += "\nComponentes por tipo:\n"
                for comp_type, count in summary['components_by_type'].items():
                    text += f"  • {comp_type}: {count}\n"

            self.summary_text.setPlainText(text)

        except Exception as e:
            logger.error(f"Error cargando resumen: {e}")
            self.summary_text.setPlainText(f"Error: {str(e)}")

    def on_browse_export(self):
        """Al hacer clic en examinar para exportación"""
        if not self.area_data:
            QMessageBox.warning(self, "Error", "No hay área seleccionada para exportar")
            return

        # Nombre sugerido
        safe_name = "".join(c for c in self.area_data['name'] if c.isalnum() or c in (' ', '-', '_')).strip()
        safe_name = safe_name.replace(' ', '_')
        default_name = f"area_{safe_name}.json"

        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Guardar Área",
            default_name,
            "JSON Files (*.json);;All Files (*)"
        )

        if file_path:
            self.selected_export_path = file_path
            self.export_path_display.setText(file_path)
            self.export_path_display.setStyleSheet("color: #9b59b6;")

    def on_export(self):
        """Al hacer clic en exportar"""
        if not self.area_data:
            QMessageBox.warning(self, "Error", "No hay área seleccionada para exportar")
            return

        try:
            # Verificar si hay ruta seleccionada
            if not self.selected_export_path:
                # Usar ruta por defecto
                safe_name = "".join(c for c in self.area_data['name'] if c.isalnum() or c in (' ', '-', '_')).strip()
                safe_name = safe_name.replace(' ', '_')
                self.selected_export_path = f"area_{safe_name}.json"

            # Exportar
            result = self.export_manager.export_area(
                self.area_data['id'],
                self.selected_export_path
            )

            if result:
                logger.info(f"Área exportada exitosamente: {result}")
                self.export_completed.emit(result)

                QMessageBox.information(
                    self,
                    "Exportación Exitosa",
                    f"Área exportada a:\n{result}"
                )
            else:
                QMessageBox.warning(
                    self,
                    "Error",
                    "No se pudo exportar el área. Revisa el log para más detalles."
                )

        except Exception as e:
            logger.error(f"Error en exportación: {e}", exc_info=True)
            QMessageBox.critical(
                self,
                "Error",
                f"Error al exportar:\n{str(e)}"
            )

    def on_browse_import(self):
        """Al hacer clic en examinar para importación"""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Seleccionar Archivo de Área",
            "",
            "JSON Files (*.json);;All Files (*)"
        )

        if file_path:
            self.selected_import_file = file_path
            self.import_file_display.setText(file_path)
            self.import_file_display.setStyleSheet("color: #9b59b6;")

            # Cargar preview
            self.load_import_preview()

    def load_import_preview(self):
        """Carga la vista previa del archivo de importación"""
        if not self.selected_import_file:
            return

        try:
            with open(self.selected_import_file, 'r', encoding='utf-8') as f:
                self.import_file_data = json.load(f)

            # Construir preview
            text = ""

            if 'area' in self.import_file_data:
                area = self.import_file_data['area']
                text += f"Área: {area.get('icon', '🏢')} {area.get('name', 'Sin nombre')}\n"
                text += f"Descripción: {area.get('description', 'Sin descripción')}\n"
                text += f"Color: {area.get('color', '#9b59b6')}\n\n"

            if 'relations' in self.import_file_data:
                relations = self.import_file_data['relations']
                text += f"Relaciones: {len(relations)}\n"

                # Contar por tipo
                by_type = {}
                for rel in relations:
                    entity_type = rel.get('entity_type', 'unknown')
                    by_type[entity_type] = by_type.get(entity_type, 0) + 1

                for entity_type, count in by_type.items():
                    text += f"  • {entity_type}: {count}\n"

                text += "\n"

            if 'components' in self.import_file_data:
                components = self.import_file_data['components']
                text += f"Componentes: {len(components)}\n"

                # Contar por tipo
                by_type = {}
                for comp in components:
                    comp_type = comp.get('component_type', 'unknown')
                    by_type[comp_type] = by_type.get(comp_type, 0) + 1

                for comp_type, count in by_type.items():
                    text += f"  • {comp_type}: {count}\n"

            if 'export_date' in self.import_file_data:
                text += f"\nFecha de exportación: {self.import_file_data['export_date']}"

            self.import_preview_text.setPlainText(text)

        except Exception as e:
            logger.error(f"Error cargando preview: {e}")
            self.import_preview_text.setPlainText(f"Error leyendo archivo:\n{str(e)}")

    def on_import(self):
        """Al hacer clic en importar"""
        if not self.selected_import_file:
            QMessageBox.warning(
                self,
                "Error",
                "Selecciona un archivo JSON para importar"
            )
            return

        try:
            # Importar
            mode = 'new' if self.new_area_radio.isChecked() else 'merge'

            area_id = self.export_manager.import_area(
                self.selected_import_file,
                import_mode=mode
            )

            if area_id:
                logger.info(f"Área importada exitosamente: ID {area_id}")
                self.import_completed.emit(area_id)

                area_name = self.import_file_data.get('area', {}).get('name', 'Área')

                QMessageBox.information(
                    self,
                    "Importación Exitosa",
                    f"Área '{area_name}' importada exitosamente.\n\nID: {area_id}"
                )
            else:
                QMessageBox.warning(
                    self,
                    "Error",
                    "No se pudo importar el área. Revisa el log para más detalles."
                )

        except Exception as e:
            logger.error(f"Error en importación: {e}", exc_info=True)
            QMessageBox.critical(
                self,
                "Error",
                f"Error al importar:\n{str(e)}"
            )
