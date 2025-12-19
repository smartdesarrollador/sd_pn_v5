# CLAUDE.md

Guía para Claude Code al trabajar con este repositorio.

## Descripción del Proyecto

**SidePanel** es una aplicación de escritorio empresarial para Windows que funciona como gestor avanzado de productividad, portapapeles y biblioteca de snippets. Construida con PyQt6 y SQLite, proporciona un sidebar persistente siempre visible para acceso instantáneo a comandos, URLs, código, procesos automatizados y gestión organizacional completa.

**Versión:** 3.0.0 (SQLite Edition)
**Plataforma:** Windows 10/11
**Python:** 3.10+
**Complejidad:** 43+ managers, 150+ vistas, 16 modelos, 40+ tablas BD, 19+ migraciones

### Características Principales

- **Gestión de Contenido**: Items (TEXT/URL/CODE/PATH), Listas, Tablas, Componentes visuales, Procesos automatizados
- **Organización Multi-Nivel**: Categorías → Proyectos/Áreas → Tags globales → Colecciones inteligentes
- **Búsqueda**: Universal (FTS5), Avanzada (multi-criterio), Global (tiempo real)
- **Seguridad**: Autenticación (bcrypt), Sesiones (24h), Cifrado Fernet transparente
- **Productividad**: Procesos, Screenshots, Galería, Navegador embebido, Notebooks
- **UI**: Sidebar persistente (70px), Paneles flotantes/fijados, Dashboard estadístico
- **Características**: Hotkey global `Ctrl+Shift+V`, Exportación/Importación, Wizards IA, System tray

## Comandos de Desarrollo

```bash
# Ejecutar aplicación
python main.py

# Construir ejecutable
build.bat

# Instalar dependencias
pip install -r requirements.txt
```

**Dependencias principales:**
- PyQt6 (6.7.0), PyQt6-WebEngine (6.7.0)
- cryptography (41.0.7), bcrypt
- pyperclip (1.9.0), pynput (1.7.7)
- matplotlib (3.8.0), Pillow (10.1.0)

## Arquitectura

### Patrón MVC

- **Models** (`src/models/`): 16 modelos (Category, Item, Lista, Table, Process, Project, Area, Tags, Drafts, etc.)
- **Views** (`src/views/`): 150+ componentes UI organizados en ventanas principales, diálogos, widgets, dashboard, búsqueda avanzada, galería
- **Controllers** (`src/controllers/`): 9 controladores (MainController, ClipboardController, ProcessController, TableController, etc.)

### Core Managers (`src/core/`) - 43+ Managers

**Categorías principales:**
- **Contenido**: config_manager, table_manager, item_validation_service, component_manager
- **Proyectos/Áreas**: project_manager, area_manager, *_filter_engine, *_export_manager, *_element_tag_manager
- **Tags**: global_tag_manager, category_tag_manager, tag_groups_manager, smart_collections_manager
- **Búsqueda**: universal_search_engine, search_engine, advanced_filter_engine, category_filter_engine
- **Seguridad**: auth_manager, session_manager, encryption_manager, master_password_manager
- **Productividad**: process_manager, process_executor, screenshot_manager, notebook_manager
- **Navegador**: browser_session_manager, browser_profile_manager, speed_dial_generator
- **Estadísticas**: usage_tracker, stats_manager, dashboard_manager, favorites_manager
- **UI**: floating_panels_manager, pinned_panels_manager, notification_manager
- **Sistema**: clipboard_manager, hotkey_manager, tray_manager, state_manager
- **IA**: ai_bulk_manager, ai_table_manager

### Base de Datos (`src/database/`)

**Archivo:** `widget_sidebar.db` (40+ tablas SQLite con FTS5)

**Tablas principales:**
- **Sistema**: settings, sessions, panel_settings
- **Contenido**: categories, items, listas, tables, clipboard_history, item_usage_history, item_drafts
- **Organización**: projects, project_relations, areas, area_relations, *_components, *_element_tags
- **Tags**: tag_groups, item_tags, category_tags, smart_collections
- **Procesos**: processes, process_items, process_execution_history
- **Navegador**: browser_config, browser_profiles, browser_sessions, bookmarks, speed_dials
- **Búsqueda**: fts_items, search_history
- **Paneles**: pinned_panels, pinned_process_panels
- **Notebooks**: notebook_tabs

**Importante:**
- Usar `check_same_thread=False` para compatibilidad PyQt6
- Transacciones: `with db.transaction() as conn:`
- Items sensibles: cifrado/descifrado automático con `is_sensitive=True`

### Flujo de Aplicación

1. `main.py` → logging, rutas frozen/script
2. QApplication
3. Autenticación: SessionManager → FirstTimeWizard/LoginDialog
4. MainController → ConfigManager → SQLite
5. MainWindow + hotkey/tray managers
6. Carga UI del sidebar

### Jerarquía de Organización (5 Niveles)

```
Items (TEXT/URL/CODE/PATH)
  ↓
Listas/Tablas
  ↓
Categorías
  ↓
Proyectos/Áreas
  ↓
Búsqueda Universal (FTS5)
```

## Detalles Clave de Implementación

### Seguridad
- **Contraseña maestra**: bcrypt hash, derivación PBKDF2
- **Cifrado**: Fernet (simétrico), transparente en BD, clave en `.env`
- **Sesiones**: 24h expiración automática

### Búsqueda Multi-Nivel
1. **Universal (FTS5)**: `universal_search_engine.py` - Full-text search en toda la app
2. **Avanzada**: `advanced_search/` - Vistas lista/tabla/árbol, multi-criterio
3. **Global**: `global_search_panel.py` - Tiempo real, debouncing 300ms
4. **Por Categoría**: `search_bar.py` - Filtrado dentro de categoría activa

### Sistema de Tracking
- **Usage Tracking**: `item_usage_history` - timestamps, tiempo ejecución, éxito/fallo
- **Estadísticas**: Items populares, olvidados, sugerencias de favoritos
- **Favoritos**: `is_favorite` + `favorite_order`

### Tags Multi-Nivel
- **Globales**: Reutilizables en toda la app
- **Items**: Múltiples tags por item
- **Categorías**: Tags específicos de categorías
- **Proyectos/Áreas**: Tags de elementos dentro de entidades
- **Grupos**: Jerarquía de tags con `tag_groups`

### Sistema de Paneles
- **Hotkey global**: `Ctrl+Shift+V` (pynput en thread de fondo)
- **System Tray**: Minimiza en lugar de cerrar
- **Paneles flotantes**: Categorías, procesos, favoritos, estadísticas
- **Paneles fijados**: Persistencia de posición con shortcuts

## Estructura del Proyecto

```
widget_sidebar/
├── main.py                         # Punto de entrada
├── widget_sidebar.db               # Base de datos SQLite (40+ tablas)
├── requirements.txt                # Dependencias
├── build.bat                       # Build PyInstaller
├── .env                            # Clave cifrado (auto-generada)
├── CLAUDE.md                       # Esta guía
│
└── src/
    ├── models/                     # 16 modelos de datos
    ├── views/                      # 150+ vistas UI
    │   ├── dialogs/                # 30+ diálogos especializados
    │   ├── widgets/                # 40+ widgets reutilizables
    │   ├── dashboard/              # Dashboard de estructura
    │   ├── advanced_search/        # Búsqueda avanzada multi-vista
    │   └── image_gallery/          # Galería de imágenes
    │
    ├── controllers/                # 9 controladores
    ├── core/                       # 43+ managers especializados
    ├── database/                   # BD + 19+ migraciones
    ├── utils/                      # Utilidades
    └── styles/                     # Estilos y temas
│
└── util/                           # Archivos temporales (NO en git)
    ├── test_*.py                   # Scripts de prueba
    ├── debug_*.py                  # Scripts de debug
    └── migrate_*.py                # Migraciones one-time
```

## Convenciones Importantes

### Organización de Archivos
**TODOS los archivos temporales van en `util/`** (excluido de git):
- Scripts: `test_*.py`, `debug_*.py`, `demo_*.py`, `migrate_*.py`, `populate_*.py`, `check_*.py`, `fix_*.py`
- Documentación: `FASE*.md`, `GUIA_*.md`
- Solo en raíz: `main.py` + archivos de configuración + documentación oficial

### Rutas y Ejecución
```python
if getattr(sys, 'frozen', False):
    base_dir = Path(sys.executable).parent  # Ejecutando como exe
else:
    base_dir = Path(__file__).parent        # Ejecutando como script
```

### Base de Datos
- **Transacciones**: `with db.transaction() as conn:`
- **Caché**: Llamar `controller.invalidate_filter_cache()` después de modificaciones
- **Cifrado**: Automático con `is_sensitive=True`

### Logging
- Archivo: `widget_sidebar_error.log`
- Nivel: DEBUG
- En cada módulo: `logger = logging.getLogger(__name__)`

## Tareas Comunes

### Agregar Categoría
```python
category_id = db.add_category(name='Nueva Categoría', icon='🆕', is_predefined=False)
```

### Agregar Item
```python
# Item regular
item_id = db.add_item(category_id=cat_id, label='Mi Comando', content='git status', item_type='CODE')

# Item sensible (auto-cifrado)
item_id = db.add_item(category_id=cat_id, label='API Key', content='sk-123', item_type='TEXT', is_sensitive=True)
```

### Trabajar con Tags
```python
item_id = db.add_item(
    category_id=cat_id,
    label='Script Python',
    content='import asyncio...',
    item_type='CODE',
    tags=['python', 'async', 'backend']
)
```

### Gestión de Sesiones
```python
from core.session_manager import SessionManager
session_mgr = SessionManager()
if session_mgr.validate_session():
    print("Sesión válida")
```

## Archivos Clave para Modificaciones

**Nuevas características:**
- `src/controllers/main_controller.py` - Orquestación
- `src/views/main_window.py` - UI principal
- `src/database/db_manager.py` - BD
- `src/core/config_manager.py` - Configuración

**Búsqueda:**
- `src/core/universal_search_engine.py` - FTS5
- `src/views/advanced_search/` - UI avanzada

**Proyectos/Áreas:**
- `src/core/project_manager.py`, `src/core/area_manager.py`
- `src/views/projects_window.py`, `src/views/areas_window.py`

**Procesos:**
- `src/core/process_manager.py`, `src/core/process_executor.py`
- `src/views/processes_floating_panel.py`

## Señales PyQt6 Principales

- `category_selected(str)`, `item_selected(Item)`, `item_copied(Item)`
- `process_state_changed()`, `filters_applied()`, `favorites_updated()`
- `project_modified()`, `area_modified()`
- `search_query_changed(str)`, `panel_toggled(bool)`, `item_usage_tracked(int)`

## Puntos de Atención

1. **Complejidad alta**: Entender dependencias antes de modificar
2. **Leer código existente**: Siempre antes de hacer cambios
3. **Arquitectura MVC**: No mezclar lógica en vistas
4. **Caché LRU**: Para operaciones costosas
5. **Migraciones**: Crear en `src/database/migrations/` para cambios de esquema
6. **Archivos temporales**: TODO en `util/`
7. **Transacciones BD**: Usar context managers
8. **Cifrado**: Transparente con `is_sensitive=True`

---

## ⚠️ CRÍTICO: Preparación para PyInstaller

**Este proyecto está LISTO para generar ejecutable.** Para mantenerlo así, sigue estas reglas estrictamente:

### Regla 1: SIEMPRE usar prefijo `src.` en imports

**❌ NUNCA hacer esto:**
```python
from core.config_manager import ConfigManager
from controllers.main_controller import MainController
from models.item import Item
from views.main_window import MainWindow
from database.db_manager import DBManager
from utils.validators import validate_email
```

**✅ SIEMPRE hacer esto:**
```python
from src.core.config_manager import ConfigManager
from src.controllers.main_controller import MainController
from src.models.item import Item
from src.views.main_window import MainWindow
from src.database.db_manager import DBManager
from src.utils.validators import validate_email
```

**Por qué**: PyInstaller requiere imports explícitos con el prefijo del paquete raíz para detectar todos los módulos necesarios.

### Regla 2: NO manipular sys.path

**❌ NUNCA hacer esto:**
```python
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))
sys.path.append(str(Path(__file__).parent))
```

**✅ En su lugar:** Usar imports con prefijo `src.` (ver Regla 1)

**Por qué**: Las manipulaciones de `sys.path` interfieren con el empaquetado de PyInstaller y crean problemas de resolución de módulos.

### Regla 3: Mantener requirements.txt actualizado

Si agregas una nueva dependencia, **SIEMPRE** actualiza `requirements.txt`:

```bash
# Después de hacer pip install nueva-libreria
pip freeze | grep nueva-libreria >> requirements.txt
```

**Dependencias CRÍTICAS que deben estar:**
- `bcrypt==4.0.1` - Autenticación
- `pyinstaller==6.3.0` - Build del ejecutable
- `mss==9.0.1` - Screenshots
- `PyQt6==6.7.0` - Framework UI

### Regla 4: NO modificar archivos de configuración de build

**Archivos que NO deben modificarse sin verificación:**
- `widget_sidebar.spec` - Configuración de PyInstaller
- `build.bat` - Script de build
- `util/pre_build_check.py` - Verificación pre-build
- `util/fix_imports.py` - Corrección de imports

### Regla 5: Verificar antes de commit

Antes de hacer commit de archivos nuevos en `src/`, ejecuta:

```bash
# Verificar que todo está correcto
python util/pre_build_check.py
```

**Salida esperada:**
```
Total de verificaciones: 10
Exitosas: 10
Fallidas: 0

[EXITO] Proyecto listo para generar ejecutable!
```

### Regla 6: Corrección automática de imports

Si accidentalmente creaste archivos con imports incorrectos:

```bash
# Corregir automáticamente todos los imports
python util/fix_imports.py

# Verificar que quedó bien
python util/pre_build_check.py
```

### Script de Generación de Ejecutable

Cuando necesites generar el ejecutable:

```bash
# Opción 1: Script automático (recomendado)
build.bat

# Opción 2: Comando directo
.\venv\Scripts\pyinstaller.exe widget_sidebar.spec --clean --noconfirm

# Ubicación del ejecutable generado:
# dist\WidgetSidebar\WidgetSidebar.exe
```

### Problemas Comunes y Soluciones

| Problema | Causa | Solución |
|----------|-------|----------|
| ModuleNotFoundError al ejecutar .exe | Imports sin prefijo `src.` | Ejecutar `python util/fix_imports.py` |
| Falta módulo en ejecutable | No está en hiddenimports de .spec | Agregar a `widget_sidebar.spec` |
| Error de PyQt6.QtNetwork | Binario no incluido | Ya está resuelto en .spec actual |
| Build falla | Dependencia no instalada en venv | `.\venv\Scripts\python.exe -m pip install -r requirements.txt` |

### Checklist de Nuevo Archivo Python

Cuando crees un nuevo archivo `.py` en `src/`:

- [ ] ✅ Todos los imports usan prefijo `src.`
- [ ] ✅ NO hay líneas `sys.path.insert()` o `sys.path.append()`
- [ ] ✅ Ejecutaste `python util/pre_build_check.py` y pasó
- [ ] ✅ Si usa una nueva librería, actualizaste `requirements.txt`

### Estado Actual del Proyecto

**✅ VERIFICADO (19-Dic-2025):**
- ✅ 392 imports corregidos con prefijo `src.`
- ✅ requirements.txt completo (bcrypt, pyinstaller incluidos)
- ✅ widget_sidebar.spec configurado correctamente
- ✅ build.bat usando venv correctamente
- ✅ Todas las verificaciones pasando (10/10)
- ✅ Entorno virtual configurado con todas las dependencias

**El proyecto está 100% listo para generar el ejecutable en cualquier momento.**
