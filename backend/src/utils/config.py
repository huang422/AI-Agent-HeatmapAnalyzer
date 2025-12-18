"""
Configuration and Constants
Centralized configuration for the backend application.
"""

import os
import sys
from pathlib import Path
from typing import Optional


def get_base_path() -> Path:
    """
    Get base path for resources.

    Works in both development and PyInstaller packaged modes.
    In PyInstaller, resources are extracted to sys._MEIPASS.
    """
    if getattr(sys, 'frozen', False):
        # Running in PyInstaller bundle
        return Path(sys._MEIPASS)
    else:
        # Running in development
        # Navigate from backend/src/utils/ to project root
        return Path(__file__).parent.parent.parent.parent


# Paths
BASE_PATH = get_base_path()
DATA_PATH = BASE_PATH / "data" / "data.csv"


# TWD97 TM2 Coordinate System Parameters
TWD97_PARAMS = {
    'a': 6378137,  # WGS84 ellipsoid semi-major axis (meters)
    'f': 1 / 298.257222101,  # Flattening
    'K': 0.9999,  # Scale factor
    'clng': 121.0,  # Central meridian (degrees)
    'FalseEasting': 250000,  # False easting (meters)
}

# Grid Parameters
GRID_PARAMS = {
    'sw_lat_offset': -32871.4054,  # Southwest corner latitude offset (meters)
    'sw_lng_offset': 2422126.0017,  # Southwest corner longitude offset (meters)
    'cell_size': 50,  # Grid cell size (meters)
}

# API Configuration
API_CONFIG = {
    'host': os.getenv('API_HOST', '127.0.0.1'),
    'port': int(os.getenv('API_PORT', '8000')),
    'reload': os.getenv('API_RELOAD', 'false').lower() == 'true',
    'log_level': os.getenv('LOG_LEVEL', 'info'),
}

# CORS Configuration
CORS_CONFIG = {
    'allow_origins': [
        "http://localhost:5173",  # Vite dev server
        "http://127.0.0.1:5173",
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    'allow_credentials': True,
    'allow_methods': ["*"],
    'allow_headers': ["*"],
}

# Ollama Configuration
OLLAMA_HOST = os.getenv('OLLAMA_HOST', 'http://localhost:11434')
OLLAMA_MODEL = os.getenv('OLLAMA_MODEL', 'qwen3:14b')


# Metric labels (Chinese)
METRIC_LABELS = {
    "avg_total_users": "全部停留人數",
    "avg_users_under_10min": "停留10分鐘以下",
    "avg_users_10_30min": "停留10-30分鐘",
    "avg_users_over_30min": "停留30分鐘以上"
}

# Age group labels (Chinese)
AGE_LABELS = {
    'age_1': '19歲以下',
    'age_2': '20-24歲',
    'age_3': '25-29歲',
    'age_4': '30-34歲',
    'age_5': '35-39歲',
    'age_6': '40-44歲',
    'age_7': '45-49歲',
    'age_8': '50-54歲',
    'age_9': '55-59歲',
    'age_other': '60歲以上'
}

# Gender labels (Chinese)
GENDER_LABELS = {
    'male': '男性',
    'female': '女性'
}


def get_data_path() -> Path:
    """
    Get path to data.csv file.

    Returns:
        Path object pointing to data.csv

    Raises:
        FileNotFoundError: If data.csv doesn't exist
    """
    if not DATA_PATH.exists():
        raise FileNotFoundError(f"Data file not found: {DATA_PATH}")
    return DATA_PATH

