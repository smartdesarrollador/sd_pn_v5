"""
Estilos CSS centralizados para vista completa de proyectos

MODO OSCURO ÚNICAMENTE - Estilos optimizados para legibilidad

Autor: Widget Sidebar Team
Versión: 1.0
"""

from .color_palette import FullViewColorPalette as Colors


class FullViewStyles:
    """
    Estilos CSS centralizados para vista completa

    Proporciona métodos estáticos para obtener estilos CSS
    de todos los componentes de la vista completa.
    """

    @staticmethod
    def get_main_panel_style():
        """Estilos para el panel principal (ProjectFullViewPanel)"""
        return f"""
            ProjectFullViewPanel {{
                background-color: {Colors.BG_MAIN};
                border: none;
            }}

            QScrollArea {{
                border: none;
                background-color: {Colors.BG_MAIN};
            }}

            QScrollBar:vertical {{
                background-color: {Colors.SCROLLBAR_BG};
                width: 12px;
                border-radius: 6px;
                margin: 0px;
            }}

            QScrollBar::handle:vertical {{
                background-color: {Colors.SCROLLBAR_HANDLE};
                border-radius: 6px;
                min-height: 30px;
            }}

            QScrollBar::handle:vertical:hover {{
                background-color: {Colors.SCROLLBAR_HANDLE_HOVER};
            }}

            QScrollBar::add-line:vertical,
            QScrollBar::sub-line:vertical {{
                border: none;
                background: none;
                height: 0px;
            }}

            QScrollBar::add-page:vertical,
            QScrollBar::sub-page:vertical {{
                background: none;
            }}
        """

    @staticmethod
    def get_project_header_style():
        """Estilos para ProjectHeaderWidget"""
        return f"""
            ProjectHeaderWidget {{
                background-color: transparent;
                border: none;
                padding: 20px 15px;
            }}

            QLabel#project_title {{
                color: {Colors.TITLE_PROJECT};
                font-size: 20px;
                font-weight: bold;
                font-family: 'Segoe UI', Arial, sans-serif;
            }}
        """

    @staticmethod
    def get_tag_header_style():
        """Estilos para ProjectTagHeaderWidget"""
        return f"""
            ProjectTagHeaderWidget {{
                background-color: transparent;
                border-left: 3px solid {Colors.TITLE_TAG};
                padding: 15px 15px 15px 20px;
                margin-top: 10px;
            }}

            QLabel#tag_title {{
                color: {Colors.TITLE_TAG};
                font-size: 18px;
                font-weight: 600;
                font-family: 'Segoe UI', Arial, sans-serif;
            }}

            QLabel#tag_count {{
                color: {Colors.TEXT_SECONDARY};
                font-size: 14px;
            }}
        """

    @staticmethod
    def get_group_header_style():
        """Estilos para GroupHeaderWidget"""
        return f"""
            GroupHeaderWidget {{
                background-color: transparent;
                padding: 10px 15px 10px 40px;
            }}

            QLabel#group_title {{
                color: {Colors.TITLE_GROUP};
                font-size: 16px;
                font-weight: 600;
                font-family: 'Consolas', 'Courier New', monospace;
            }}
        """

    @staticmethod
    def get_text_item_style():
        """Estilos para TextItemWidget"""
        return f"""
            TextItemWidget {{
                background-color: {Colors.BG_ITEM_TEXT};
                border: 1px solid {Colors.BORDER_DEFAULT};
                border-radius: 6px;
                padding: 12px;
                margin: 8px 15px 8px 60px;
            }}

            TextItemWidget:hover {{
                background-color: {Colors.BG_HOVER};
                border-color: {Colors.ACCENT};
            }}

            QLabel#text_content {{
                color: {Colors.TEXT_PRIMARY};
                font-size: 13px;
                line-height: 1.6;
                font-family: 'Segoe UI', Arial, sans-serif;
            }}

            QTextEdit#text_content {{
                background-color: transparent;
                border: none;
                color: {Colors.TEXT_PRIMARY};
                font-size: 13px;
                line-height: 1.6;
                font-family: 'Segoe UI', Arial, sans-serif;
            }}

            QTextEdit#text_content QScrollBar:vertical {{
                background-color: {Colors.SCROLLBAR_BG};
                width: 8px;
                border-radius: 4px;
            }}

            QTextEdit#text_content QScrollBar::handle:vertical {{
                background-color: {Colors.SCROLLBAR_HANDLE};
                border-radius: 4px;
                min-height: 20px;
            }}

            QTextEdit#text_content QScrollBar::handle:vertical:hover {{
                background-color: {Colors.SCROLLBAR_HANDLE_HOVER};
            }}

            QTextEdit#text_content QScrollBar:horizontal {{
                background-color: {Colors.SCROLLBAR_BG};
                height: 8px;
                border-radius: 4px;
            }}

            QTextEdit#text_content QScrollBar::handle:horizontal {{
                background-color: {Colors.SCROLLBAR_HANDLE};
                border-radius: 4px;
                min-width: 20px;
            }}

            QTextEdit#text_content QScrollBar::handle:horizontal:hover {{
                background-color: {Colors.SCROLLBAR_HANDLE_HOVER};
            }}

            QTextEdit#text_content QScrollBar::add-line,
            QTextEdit#text_content QScrollBar::sub-line {{
                border: none;
                background: none;
            }}
        """

    @staticmethod
    def get_code_item_style():
        """Estilos para CodeItemWidget"""
        return f"""
            CodeItemWidget {{
                background-color: {Colors.BG_ITEM_CODE};
                border: 1px solid {Colors.BORDER_CODE};
                border-radius: 6px;
                padding: 12px;
                margin: 8px 15px 8px 60px;
            }}

            CodeItemWidget:hover {{
                background-color: #141920;
                border-color: {Colors.TEXT_CODE};
            }}

            QTextEdit#code_content {{
                background-color: transparent;
                border: none;
                color: {Colors.TEXT_CODE};
                font-family: 'Consolas', 'Courier New', monospace;
                font-size: 12px;
                selection-background-color: {Colors.BORDER_CODE};
            }}

            QTextEdit#code_content QScrollBar:vertical {{
                background-color: {Colors.SCROLLBAR_BG};
                width: 8px;
                border-radius: 4px;
            }}

            QTextEdit#code_content QScrollBar::handle:vertical {{
                background-color: {Colors.SCROLLBAR_HANDLE};
                border-radius: 4px;
                min-height: 20px;
            }}

            QTextEdit#code_content QScrollBar::handle:vertical:hover {{
                background-color: {Colors.SCROLLBAR_HANDLE_HOVER};
            }}

            QTextEdit#code_content QScrollBar:horizontal {{
                background-color: {Colors.SCROLLBAR_BG};
                height: 8px;
                border-radius: 4px;
            }}

            QTextEdit#code_content QScrollBar::handle:horizontal {{
                background-color: {Colors.SCROLLBAR_HANDLE};
                border-radius: 4px;
                min-width: 20px;
            }}

            QTextEdit#code_content QScrollBar::handle:horizontal:hover {{
                background-color: {Colors.SCROLLBAR_HANDLE_HOVER};
            }}

            QTextEdit#code_content QScrollBar::add-line,
            QTextEdit#code_content QScrollBar::sub-line {{
                border: none;
                background: none;
            }}
        """

    @staticmethod
    def get_url_item_style():
        """Estilos para URLItemWidget"""
        return f"""
            URLItemWidget {{
                background-color: {Colors.BG_ITEM_URL};
                border: 1px solid {Colors.BORDER_URL};
                border-radius: 6px;
                padding: 12px;
                margin: 8px 15px 8px 60px;
            }}

            URLItemWidget:hover {{
                background-color: #232342;
                border-color: {Colors.TEXT_URL};
            }}

            QLabel#url_text {{
                color: {Colors.TEXT_URL};
                font-size: 13px;
                text-decoration: underline;
                font-family: 'Segoe UI', Arial, sans-serif;
            }}

            QLabel#url_text:hover {{
                color: #6BB6FF;
            }}

            QTextEdit#url_text {{
                background-color: transparent;
                border: none;
                color: {Colors.TEXT_URL};
                font-size: 13px;
                font-family: 'Segoe UI', Arial, sans-serif;
            }}

            QTextEdit#url_text QScrollBar:vertical {{
                background-color: {Colors.SCROLLBAR_BG};
                width: 8px;
                border-radius: 4px;
            }}

            QTextEdit#url_text QScrollBar::handle:vertical {{
                background-color: {Colors.SCROLLBAR_HANDLE};
                border-radius: 4px;
                min-height: 20px;
            }}

            QTextEdit#url_text QScrollBar::handle:vertical:hover {{
                background-color: {Colors.SCROLLBAR_HANDLE_HOVER};
            }}

            QTextEdit#url_text QScrollBar:horizontal {{
                background-color: {Colors.SCROLLBAR_BG};
                height: 8px;
                border-radius: 4px;
            }}

            QTextEdit#url_text QScrollBar::handle:horizontal {{
                background-color: {Colors.SCROLLBAR_HANDLE};
                border-radius: 4px;
                min-width: 20px;
            }}

            QTextEdit#url_text QScrollBar::handle:horizontal:hover {{
                background-color: {Colors.SCROLLBAR_HANDLE_HOVER};
            }}

            QTextEdit#url_text QScrollBar::add-line,
            QTextEdit#url_text QScrollBar::sub-line {{
                border: none;
                background: none;
            }}
        """

    @staticmethod
    def get_path_item_style():
        """Estilos para PathItemWidget"""
        return f"""
            PathItemWidget {{
                background-color: {Colors.BG_ITEM_PATH};
                border: 1px solid {Colors.BORDER_PATH};
                border-radius: 6px;
                padding: 12px;
                margin: 8px 15px 8px 60px;
            }}

            PathItemWidget:hover {{
                background-color: {Colors.BG_HOVER};
                border-color: {Colors.TEXT_PATH};
            }}

            QLabel#path_text {{
                color: {Colors.TEXT_PATH};
                font-family: 'Consolas', 'Courier New', monospace;
                font-size: 12px;
            }}

            QTextEdit#path_text {{
                background-color: transparent;
                border: none;
                color: {Colors.TEXT_PATH};
                font-family: 'Consolas', 'Courier New', monospace;
                font-size: 12px;
            }}

            QTextEdit#path_text QScrollBar:vertical {{
                background-color: {Colors.SCROLLBAR_BG};
                width: 8px;
                border-radius: 4px;
            }}

            QTextEdit#path_text QScrollBar::handle:vertical {{
                background-color: {Colors.SCROLLBAR_HANDLE};
                border-radius: 4px;
                min-height: 20px;
            }}

            QTextEdit#path_text QScrollBar::handle:vertical:hover {{
                background-color: {Colors.SCROLLBAR_HANDLE_HOVER};
            }}

            QTextEdit#path_text QScrollBar:horizontal {{
                background-color: {Colors.SCROLLBAR_BG};
                height: 8px;
                border-radius: 4px;
            }}

            QTextEdit#path_text QScrollBar::handle:horizontal {{
                background-color: {Colors.SCROLLBAR_HANDLE};
                border-radius: 4px;
                min-width: 20px;
            }}

            QTextEdit#path_text QScrollBar::handle:horizontal:hover {{
                background-color: {Colors.SCROLLBAR_HANDLE_HOVER};
            }}

            QTextEdit#path_text QScrollBar::add-line,
            QTextEdit#path_text QScrollBar::sub-line {{
                border: none;
                background: none;
            }}
        """

    @staticmethod
    def get_web_static_item_style():
        """Estilos para WebStaticItemWidget"""
        return f"""
            WebStaticItemWidget {{
                background-color: {Colors.BG_ITEM_CODE};
                border: 1px solid #4CAF50;
                border-radius: 6px;
                padding: 12px;
                margin: 8px 15px 8px 60px;
            }}

            WebStaticItemWidget:hover {{
                background-color: {Colors.BG_HOVER};
                border-color: #66BB6A;
            }}

            QLabel#web_content {{
                color: #90EE90;
                font-family: 'Consolas', 'Courier New', monospace;
                font-size: 12px;
            }}
        """

    @staticmethod
    def get_copy_button_style():
        """Estilos para CopyButton"""
        return f"""
            CopyButton {{
                background-color: transparent;
                border: 1px solid {Colors.BORDER_DEFAULT};
                border-radius: 4px;
                padding: 6px 10px;
                color: {Colors.TEXT_SECONDARY};
                font-size: 16px;
            }}

            CopyButton:hover {{
                background-color: {Colors.BG_HOVER};
                border-color: {Colors.ACCENT};
                color: {Colors.ACCENT};
            }}

            CopyButton:pressed {{
                background-color: {Colors.ACCENT};
                color: #FFFFFF;
            }}
        """

    @staticmethod
    def get_scrollbar_style():
        """Estilos para scrollbars genéricos"""
        return f"""
            QScrollBar:vertical {{
                background-color: {Colors.SCROLLBAR_BG};
                width: 8px;
                border-radius: 4px;
            }}

            QScrollBar::handle:vertical {{
                background-color: {Colors.SCROLLBAR_HANDLE};
                border-radius: 4px;
                min-height: 20px;
            }}

            QScrollBar::handle:vertical:hover {{
                background-color: {Colors.SCROLLBAR_HANDLE_HOVER};
            }}

            QScrollBar::add-line:vertical,
            QScrollBar::sub-line:vertical {{
                border: none;
                background: none;
            }}

            QScrollBar:horizontal {{
                height: 0px;
            }}
        """

    @classmethod
    def get_all_styles(cls) -> str:
        """
        Obtener todos los estilos combinados

        Returns:
            String con todos los estilos CSS concatenados
        """
        return "\n\n".join([
            cls.get_main_panel_style(),
            cls.get_project_header_style(),
            cls.get_tag_header_style(),
            cls.get_group_header_style(),
            cls.get_text_item_style(),
            cls.get_code_item_style(),
            cls.get_url_item_style(),
            cls.get_path_item_style(),
            cls.get_copy_button_style(),
        ])


# Test de estilos (para desarrollo)
if __name__ == '__main__':
    print("Estilos CSS para Vista Completa de Proyectos")
    print("=" * 60)
    print("\nPROJECT HEADER STYLES:")
    print(FullViewStyles.get_project_header_style())
    print("\nTAG HEADER STYLES:")
    print(FullViewStyles.get_tag_header_style())
    print("\nCODE ITEM STYLES:")
    print(FullViewStyles.get_code_item_style())
    print("=" * 60)
