from logging import getLogger

import torch
from torch import nn as nn
from torch.nn import functional as F

from app.ml.utilities import model_verify
from ..config.path_manager import PathManager

logger = getLogger(__name__)


class SimpleConv(nn.Module):
    def __init__(self):
        super(SimpleConv, self).__init__()
        self.conv1 = nn.Conv2d(1, 20, 5, 1)
        self.conv2 = nn.Conv2d(20, 50, 5, 1)
        self.fc1 = nn.Linear(4 * 4 * 50, 500)
        self.fc2 = nn.Linear(500, 10)

    def forward(self, x):
        x = F.relu(self.conv1(x))
        x = F.max_pool2d(x, 2, 2)
        x = F.relu(self.conv2(x))
        x = F.max_pool2d(x, 2, 2)
        x = x.view(-1, 4 * 4 * 50)
        x = F.relu(self.fc1(x))
        x = self.fc2(x)
        return F.log_softmax(x, dim=1)


def load_model(device, trained: bool = False) -> torch.nn.Module:
    model = SimpleConv()
    if trained:
        trained_model_path = PathManager.get_trained_model_path('mnist_cnn')
        model_verify(trained_model_path)
        model.load_state_dict(torch.load(str(PathManager.MODEL_DIR / trained_model_path)))
        logger.info(f'trained model loaded: {trained_model_path}')

    model.to(device)
    return model
