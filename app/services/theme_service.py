import os
import json
from typing import Optional


def _theme_file_path() -> str:
    """Ruta del archivo de configuración del tema."""
    # app/services/theme_service.py -> root -> storage/data/theme.json
    root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    project_root = os.path.abspath(os.path.join(root_dir, ".."))
    data_dir = os.path.join(project_root, "storage", "data")
    os.makedirs(data_dir, exist_ok=True)
    return os.path.join(data_dir, "theme.json")


def load_theme_preference() -> bool:
    """Carga la preferencia de tema oscuro desde el archivo."""
    try:
        path = _theme_file_path()
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
                return data.get("dark_mode", False)
        return False  # Por defecto tema claro
    except Exception:
        return False


def save_theme_preference(dark_mode: bool) -> bool:
    """Guarda la preferencia de tema oscuro en el archivo."""
    try:
        path = _theme_file_path()
        data = {"dark_mode": dark_mode}
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        return True
    except Exception:
        return False


def toggle_theme() -> bool:
    """Alterna entre tema claro y oscuro. Retorna el nuevo estado."""
    current = load_theme_preference()
    new_state = not current
    save_theme_preference(new_state)
    return new_state
