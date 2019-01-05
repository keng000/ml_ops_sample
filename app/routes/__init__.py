import os
from logging import getLogger, StreamHandler, INFO, DEBUG

from flask import Flask

# setup stream logger
logger = getLogger()
handler = StreamHandler()
handler.setLevel(INFO)
logger.setLevel(INFO)
logger.addHandler(handler)

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

env_USE_GPU = os.getenv('USE_GPU')
USE_GPU = not (env_USE_GPU is None or env_USE_GPU == '0')
DEVICE = 'cuda' if USE_GPU else 'cpu'
MODEL = load_model(device=DEVICE, trained=True)
