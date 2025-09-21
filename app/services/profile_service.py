import os
import json
from typing import Optional


def _project_root() -> str:
    # This file is in app/services -> go up 2 levels to repo root
    return os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))


def _data_dir() -> str:
    d = os.path.join(_project_root(), "storage", "data")
    os.makedirs(d, exist_ok=True)
    return d


def profile_file_path() -> str:
    return os.path.join(_data_dir(), "profile.json")


def load_profile() -> Optional[dict]:
    p = profile_file_path()
    if not os.path.exists(p):
        return None
    try:
        with open(p, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return None


def save_profile(data: dict) -> None:
    p = profile_file_path()
    with open(p, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def has_profile_data() -> bool:
    data = load_profile()
    if not data:
        return False
    required = {"weight_kg", "height_cm", "daily_goal_ml"}
    return required.issubset(data.keys())


def delete_profile() -> bool:
    """Elimina el archivo de perfil. Retorna True si se eliminó o no existía."""
    p = profile_file_path()
    try:
        if os.path.exists(p):
            os.remove(p)
        return True
    except Exception:
        return False


def reset_app_data() -> bool:
    """Elimina todos los datos de la app (perfil y base de datos)."""
    try:
        # Eliminar perfil
        delete_profile()
        
        # Eliminar base de datos de ingestas
        from .intake_service import _get_db_path
        db_path = _get_db_path()
        if os.path.exists(db_path):
            os.remove(db_path)
        
        return True
    except Exception as e:
        print(f"Error al resetear datos: {e}")
        return False
