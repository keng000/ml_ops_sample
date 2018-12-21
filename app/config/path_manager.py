from pathlib import Path


class PathManager:
    APP_ROOT = Path(__file__).resolve().parents[1]
    MODEL_DIR = APP_ROOT / 'ml' / 'trained_model'
