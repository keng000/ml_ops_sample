import argparse

import torch
from PIL import Image

from app.ml.dataset import get_test_transform
from app.ml.model import load_model


def estimate(data: Image, model: torch.nn.Module, device: torch.device) -> int:
    """
    estimate a label.
    Args:
        data: PIL.Image: an image to estimate.
        model: torch.nn.Module: model to train.
        device: torch.device: specify the device to map data. should be `cuda` or `cpu`

    Returns:
        int: estimated label.
    """
    model.eval()

    transform = get_test_transform()
    data = transform(data)

    with torch.no_grad():
        data = torch.unsqueeze(data, dim=0)
        output = model(data.to(device))
        pred = output.max(1, keepdim=True)[1]  # get the index of the max log-probability
    return pred


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--image_path', action='store', required=True,
                        help='path to mnist image')
    parser.add_argument('--no-cuda', action='store_true', default=False,
                        help='disables CUDA training')
    args = parser.parse_args()
    use_cuda = not args.no_cuda and torch.cuda.is_available()
    device = torch.device("cuda" if use_cuda else "cpu")

    # load model
    model = load_model(device, trained=True)

    # load image
    image = Image.open(args.image_path)

    label = estimate(image, model, device)
    print(f"Estimated label: {int(label)}")


if __name__ == '__main__':
    main()
