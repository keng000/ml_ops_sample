import os
import unittest
import warnings
from pathlib import Path

from app.controllers import s3_downloader


@unittest.skipIf(os.getenv("CIRCLECI", False), "Skip test on circle ci.")
class TestS3Downloader(unittest.TestCase):
    def setUp(self):
        # ignore boto3 unresolved warnings
        # https://github.com/boto/boto3/issues/454
        warnings.filterwarnings("ignore", category=ResourceWarning, message="unclosed.*<ssl.SSLSocket.*>")

    def test_session(self):
        session = s3_downloader.create_session()
        path_list = set(
            element["Key"] for element in
            session.list_objects(Bucket="keng000-mlops").get("Contents"))

        self.assertTrue("alive_check" in path_list)

    def test_download(self):
        local_path = Path("./test_file")
        try:
            s3_downloader.download(Path("alive_check"), local_path)
            self.assertTrue(local_path.exists())
        finally:
            if local_path.exists():
                local_path.unlink()

    def test_download_as_temporary(self):
        local_path = Path("./test_file")

        try:
            with s3_downloader.download_as_temporary(Path("alive_check")) as tmp_file:
                with self.subTest("exists check"):
                    self.assertTrue(tmp_file.exists())

            # check tmp file is removed
            with self.subTest("removed check"):
                self.assertFalse(tmp_file.exists())

        finally:
            if local_path.exists():
                local_path.unlink()


if __name__ == '__main__':
    unittest.main()
