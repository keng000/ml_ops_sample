from typing import Tuple

from torch.utils.data import DataLoader
from torchvision import transforms, datasets


def get_data_loader(batch_size: int, test_batch_size: int, use_cuda: bool) -> Tuple[DataLoader, DataLoader]:
    train_transform = transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize((0.1307,), (0.3081,))])

    test_transform = transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize((0.1307,), (0.3081,))])

    kwargs = {'num_workers': 1, 'pin_memory': True} if use_cuda else {}

    train_loader = DataLoader(
        datasets.MNIST('./data', train=True, download=True, transform=train_transform),
        batch_size=batch_size, shuffle=True, **kwargs)

    test_loader = DataLoader(
        datasets.MNIST('./data', train=False, transform=test_transform),
        batch_size=test_batch_size, shuffle=True, **kwargs)

    return train_loader, test_loader
