import json
import unittest
from pathlib import Path
import base64

import yaml
from PIL import Image

from app.config.path_manager import PathManager
from app.routes import app


class TestAPI(unittest.TestCase):

    @classmethod
    def setUpClass(cls):

        cls.app = app.test_client()

        config_file = PathManager.get_config_file_path('api_config_local.yml')
        with config_file.open('r') as fp:
            config = yaml.load(fp)

        cls.url = f"http://{config['host']}:{config['port']}"

    def test_index(self):
        ret = self.app.get(f"{self.url}/")
        self.assertEqual(ret.status_code, 200)

    def test_health_check(self):
        ret = self.app.get(f"{self.url}/hc")
        self.assertEqual(ret.status_code, 200)

    def test_estimate(self):
        pass

