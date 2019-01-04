from pathlib import Path

import yaml


class PathManager:
    APP_ROOT = Path(__file__).resolve().parents[1]
    MODEL_DIR = APP_ROOT / 'ml' / 'trained_model'
    CONFIG_DIR = APP_ROOT / 'config'

    with (CONFIG_DIR / 'trained_model_path_list.yml').open('r') as fp:
        MODEL_PATH_LIST = yaml.load(fp)

    @staticmethod
    def get_config_file_path(filename) -> Path:
        return PathManager.CONFIG_DIR / filename

    @staticmethod
    def get_trained_model_path(module_name: str) -> Path:
        return Path(PathManager.MODEL_PATH_LIST[module_name])
