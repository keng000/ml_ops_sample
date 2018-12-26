from flask import Flask
from pathlib import Path
import yaml

app = Flask(__name__)


@app.route('/', methods=['GET'])
def index():
    return 'Hello'


@app.route('/estimate', methods=['GET', 'POST'])
def estimate():
    return 'estimate api'


@app.route('/hc', methods=['GET'])
def hc():
    return 'alive'


if __name__ == '__main__':
    config_file = Path(__file__).resolve().parents[1] / 'config' / 'api_config_local.yml'
    with config_file.open('r') as fp:
        config = yaml.load(fp)

    app.run(host=config['host'], port=config['port'])