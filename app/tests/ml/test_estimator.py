import unittest

import torch
from PIL import Image

from app.ml.estimator import estimate
from app.ml.model import load_model


class TestEstimator(unittest.TestCase):
    def test_estimate(self):
        image = Image.open('./datas/sample.jpg')

        devices = ["cpu"]
        if torch.cuda.is_available():
            devices.append("cuda")

        for device in devices:
            device = torch.device(device)
            model = load_model(device)
            with self.subTest(f"Device {device}"):
                label = estimate(data=image, model=model, device=device)
                self.assertTrue(0 <= label <= 9)


if __name__ == '__main__':
    unittest.main()
