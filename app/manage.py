import yaml

from app.config.path_manager import PathManager
from app.routes import app


if __name__ == '__main__':
    config_file = PathManager.get_config_file_path('api_config_local.yml')
    with config_file.open('r') as fp:
        config = yaml.load(fp)

    app.run(host=config['host'], port=config['port'])
