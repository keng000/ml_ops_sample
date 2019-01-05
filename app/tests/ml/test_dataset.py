import unittest
from torch.utils.data import DataLoader
from torchvision.transforms import Compose
from app.ml import dataset


class TestDataset(unittest.TestCase):
    def test_get_train_transform(self):
        train_transform = dataset.get_train_transform()
        self.assertTrue(isinstance(train_transform, Compose))

    def test_get_test_transform(self):
        test_transform = dataset.get_test_transform()
        self.assertTrue(isinstance(test_transform, Compose))

    def test_get_data_loader(self):
        train_loader, test_loader = dataset.get_data_loader(batch_size=1, test_batch_size=1, use_cuda=False)
        self.assertTrue(isinstance(train_loader, DataLoader))
        self.assertTrue(isinstance(test_loader, DataLoader))
