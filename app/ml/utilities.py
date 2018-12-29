from logging import getLogger
from pathlib import Path

from app.config.path_manager import PathManager
from app.controllers.s3_downloader import download

logger = getLogger(__name__)


def model_verify(relative_trained_model_path: Path):
    trained_model_path = PathManager.MODEL_DIR / relative_trained_model_path
    if not trained_model_path.exists():
        trained_model_path_on_s3 = Path('trained_models') / relative_trained_model_path
        download(trained_model_path_on_s3, trained_model_path)
        logger.info(f"trained model downloaded: {relative_trained_model_path}")
