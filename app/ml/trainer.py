import argparse

import torch
import torch.nn.functional as F
import torch.optim as optim

from app.config.path_manager import PathManager
from app.ml.dataset import get_data_loader
from app.ml.model import load_model


def train(model: torch.nn.Module, device: torch.device, train_loader: torch.utils.data.DataLoader,
          optimizer: torch.optim.Optimizer, epoch: int, log_interval: int):
    """
    One train iteration in training phase.
    Args:
        model: torch.nn.Module: model to train.
        device: torch.device: specify the device to map data. should be `cuda` or `cpu`
        train_loader: DataLoader: a data loader which include train data.
        optimizer: torch.optim.Optimizer:
        epoch: int: num of train epochs.
        log_interval: an interval of log output.
    """
    model.train()
    for batch_idx, (data, target) in enumerate(train_loader):
        data, target = data.to(device), target.to(device)
        optimizer.zero_grad()
        output = model(data)
        loss = F.nll_loss(output, target)
        loss.backward()
        optimizer.step()
        if batch_idx % log_interval == 0:
            print('Train Epoch: {} [{}/{} ({:.0f}%)]\tLoss: {:.6f}'.format(
                epoch, batch_idx * len(data), len(train_loader.dataset),
                       100. * batch_idx / len(train_loader), loss.item()))


def test(model: torch.nn.Module, device: torch.device, test_loader: torch.utils.data.DataLoader):
    """
    One test iteration in the training phase.
    Args:
        model: torch.nn.Module: model to train.
        device: torch.device: specify the device to map data. should be `cuda` or `cpu`
        test_loader: DataLoader: a data loader which include test data.
    """
    model.eval()
    test_loss = 0
    correct = 0
    with torch.no_grad():
        for data, target in test_loader:
            data, target = data.to(device), target.to(device)
            output = model(data)
            test_loss += F.nll_loss(output, target, reduction='sum').item()  # sum up batch loss
            pred = output.max(1, keepdim=True)[1]  # get the index of the max log-probability
            correct += pred.eq(target.view_as(pred)).sum().item()

    test_loss /= len(test_loader.dataset)

    print('\nTest set: Average loss: {:.4f}, Accuracy: {}/{} ({:.0f}%)\n'.format(
        test_loss, correct, len(test_loader.dataset),
        100. * correct / len(test_loader.dataset)))


def main():
    # Training settings
    parser = argparse.ArgumentParser()
    parser.add_argument('--batch-size', type=int, default=64, metavar='N',
                        help='input batch size for training (default: 64)')
    parser.add_argument('--test-batch-size', type=int, default=1000, metavar='N',
                        help='input batch size for testing (default: 1000)')
    parser.add_argument('--epochs', type=int, default=10, metavar='N',
                        help='number of epochs to train (default: 10)')
    parser.add_argument('--lr', type=float, default=0.01, metavar='LR',
                        help='learning rate (default: 0.01)')
    parser.add_argument('--momentum', type=float, default=0.5, metavar='M',
                        help='SGD momentum (default: 0.5)')
    parser.add_argument('--no-cuda', action='store_true', default=False,
                        help='disables CUDA training')
    parser.add_argument('--log-interval', type=int, default=10, metavar='N',
                        help='how many batches to wait before logging training status')

    args = parser.parse_args()
    use_cuda = not args.no_cuda and torch.cuda.is_available()
    device = torch.device("cuda" if use_cuda else "cpu")

    train_loader, test_loader = get_data_loader(args.batch_size, args.test_batch_size, use_cuda)
    model = load_model(device=device)
    optimizer = optim.SGD(model.parameters(), lr=args.lr, momentum=args.momentum)

    # training
    for epoch in range(1, args.epochs + 1):
        train(model, device, train_loader, optimizer, epoch, args.log_interval)
        test(model, device, test_loader)

    # model serializing
    model_dir = PathManager.MODEL_DIR
    model_dir.mkdir(parents=True, exist_ok=True)
    model_path = model_dir / "mnist_cnn.pth"
    torch.save(model.state_dict(), str(model_path))


if __name__ == '__main__':
    main()
