import base64
import sys
import tempfile
import traceback

from PIL import Image
from flask import request, jsonify

from app.routes import DEVICE, MODEL
from ..ml.estimator import estimate
from ..exceptions.data_content_exception import DataContentException
from logging import getLogger

logger = getLogger(__name__)


class EstimateAPI:
    def __init__(self):
        base64_encoded_image = self._parse_requests('image')
        base64_encoded_image = base64_encoded_image.encode()
        self.image = self.create_tmp_image_from_base64(base64_encoded_image)

    def estimate(self):
        response = {}

        try:
            estimated_label = int(estimate(self.image, model=MODEL, device=DEVICE))
            logger.info("estimate success")

            response["result"] = estimated_label
            response["status_code"] = 200
            response["message"] = "success"
            return jsonify(response)

        except DataContentException:
            t, v, tb = sys.exc_info()
            msg = "".join(traceback.format_exception(t, v, tb))
            logger.warning(msg)

            response["result"] = False
            response["status_code"] = 500
            response["message"] = "The posted data is not an image or not encoded properly"
            return jsonify(response)

        except Exception as e:
            t, v, tb = sys.exc_info()
            msg = "".join(traceback.format_exception(t, v, tb))
            logger.warning(msg)

            response["result"] = False
            response["status_code"] = 500
            response["message"] = e.args
            return jsonify(response)

    @staticmethod
    def create_tmp_image_from_base64(data: bytes) -> Image:
        """
        Create a PIL.Image object from base64 encoded data.
        Args:
            data:
                base64 encoded string
        Returns:
            PIL.Image object
        """
        decoded = base64.b64decode(data)

        with tempfile.NamedTemporaryFile() as fp:
            fp.write(decoded)
            try:
                img = Image.open(fp)

            except IOError:
                raise DataContentException('The received data is not an image.')

            img.load()
        return img

    @staticmethod
    def _parse_requests(key: str, default=None):
        m = request.method
        l = request.args
        try:
            return request.args[key]
        except KeyError:
            return default
