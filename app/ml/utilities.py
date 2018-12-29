from logging import getLogger
from pathlib import Path

from app.config.path_manager import PathManager
from app.controllers.s3_downloader import download

logger = getLogger(__name__)


def model_verify(relative_trained_model_path: Path):
    trained_model_path = PathManager.MODEL_DIR / relative_trained_model_path
    if not trained_model_path.exists():
        download(relative_trained_model_path, trained_model_path)
        logger.info(f"trained model downloaded: {relative_trained_model_path}")
