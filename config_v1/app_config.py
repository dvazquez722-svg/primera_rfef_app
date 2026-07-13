from dataclasses import dataclass
from pathlib import Path


# ==========================================================
# PATHS
# ==========================================================

ROOT_DIR = Path(__file__).resolve().parents[1]

ASSETS_DIR = ROOT_DIR / "assets"
DATA_DIR = ROOT_DIR / "data"
PAGES_DIR = ROOT_DIR / "pages"

LOGO_PATH = ASSETS_DIR / "logo.png"


# ==========================================================
# APPLICATION
# ==========================================================

APP_NAME = "Rendimiento y Control de Carga"

APP_ICON = "⚽"

PAGE_LAYOUT = "wide"

SIDEBAR_STATE = "expanded"

INITIAL_PAGE = "Estado General"


# ==========================================================
# COLORS
# ==========================================================

PRIMARY_COLOR = "#F97316"

SECONDARY_COLOR = "#111827"

SUCCESS_COLOR = "#16A34A"

WARNING_COLOR = "#F59E0B"

DANGER_COLOR = "#DC2626"

INFO_COLOR = "#2563EB"

BACKGROUND_COLOR = "#F8FAFC"

CARD_COLOR = "#FFFFFF"


# ==========================================================
# DIMENSIONS
# ==========================================================

DIMENSIONS = [

    "Disponibilidad",

    "Carga Externa",

    "Carga Interna",

    "Respuesta"

]


# ==========================================================
# GLOBAL STATES
# ==========================================================

PLAYER_STATES = [

    "Óptimo",

    "Apto",

    "Apto con adaptación",

    "Recuperación",

    "No disponible"

]


# ==========================================================
# RECOMMENDATIONS
# ==========================================================

RECOMMENDATIONS = [

    "Mantener planificación",

    "Reducir volumen",

    "Incrementar volumen",

    "Reducir intensidad",

    "Incrementar intensidad",

    "Reducir HSR",

    "Incrementar HSR",

    "Trabajo compensatorio",

    "Trabajo individual",

    "Recuperación"

]


# ==========================================================
# ICONS
# ==========================================================

ICONS = {

    "Disponibilidad": "🟢",

    "Carga Externa": "📊",

    "Carga Interna": "❤️",

    "Respuesta": "🧠",

    "Estado General": "🏠",

    "Plantilla": "👥",

    "Perfil": "👤",

    "Microciclo": "📅",

    "Riesgo": "🚨",

    "Informe": "📄"

}


# ==========================================================
# DASHBOARD CONFIGURATION
# ==========================================================

@dataclass(frozen=True)
class DashboardConfig:

    app_name: str = APP_NAME

    page_layout: str = PAGE_LAYOUT

    sidebar_state: str = SIDEBAR_STATE

    initial_page: str = INITIAL_PAGE


CONFIG = DashboardConfig()