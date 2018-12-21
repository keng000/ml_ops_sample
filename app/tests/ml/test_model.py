import unittest

import torch

from app.ml.model import load_model


class TestModel(unittest.TestCase):
    def test_load_model(self):
        devices = ["cpu"]
        if torch.cuda.is_available():
            devices.append("cuda")

        for device in devices:
            device = torch.device(device)
            with self.subTest(f"Device {device}"):
                model = load_model(device)
                self.assertTrue(isinstance(torch.nn.Module, model))


if __name__ == '__main__':
    unittest.main()
