import unittest

from app.config.path_manager import PathManager


class TestPathManager(unittest.TestCase):
    def test_get_config_file_path(self):
        filename = 'trained_model_path_list.yml'
        config_file_path = PathManager.get_config_file_path(filename)

        self.assertEqual(config_file_path, PathManager.APP_ROOT / 'config' / filename)
