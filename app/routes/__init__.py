import os
from pathlib import Path

import yaml
from flask import Flask, request

app = Flask(__name__)


@app.route('/', methods=['GET'])
def index():
    return 'Hello\n'


@app.route('/estimate', methods=['GET'])
def estimate():
    from app.controllers.estimate_api import EstimateAPI
    estimator = EstimateAPI()
    return estimator.estimate()


@app.route('/hc', methods=['GET'])
def hc():
    return 'alive'


# global variables for ML
from app.ml.model import load_model
USE_GPU = os.getenv('USE_GPU') is not None
DEVICE = 'cuda' if USE_GPU else 'cpu'
MODEL = load_model(device=DEVICE, trained=True)


if __name__ == '__main__':
    config_file = Path(__file__).resolve().parents[1] / 'config' / 'api_config_local.yml'
    with config_file.open('r') as fp:
        config = yaml.load(fp)

    from logging import getLogger, StreamHandler, DEBUG

    logger = getLogger()
    handler = StreamHandler()
    handler.setLevel(DEBUG)
    logger.setLevel(DEBUG)
    logger.addHandler(handler)

    app.run(host=config['host'], port=config['port'])
