import unittest

import torch

from app.config.path_manager import PathManager
from app.ml.model import load_model


class TestModel(unittest.TestCase):
    def test_load_model(self):
        trained_model_path = PathManager.MODEL_DIR / PathManager.get_trained_model_path('mnist_cnn')
        trained_model_path.unlink()

        devices = ["cpu"]
        if torch.cuda.is_available():
            devices.append("cuda")

        for device in devices:
            device = torch.device(device)
            with self.subTest(f"Device {device}"):
                model = load_model(device, trained=True)
                self.assertTrue(isinstance(model, torch.nn.Module))
