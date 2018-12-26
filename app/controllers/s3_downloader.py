import os
import tempfile
from contextlib import contextmanager
from logging import getLogger
from pathlib import Path
from typing import Union

import boto3

logger = getLogger(__name__)


def get_keys():
    AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID', None)
    if AWS_ACCESS_KEY_ID is None:
        raise AttributeError('env variable AWS_ACCESS_KEY_ID are not set.')

    AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY', None)
    if AWS_SECRET_ACCESS_KEY is None:
        raise AttributeError('env variable AWS_SECRET_ACCESS_KEY are not set.')

    return AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY


def download(src_path_in_s3: Union[str, Path], dst_path_in_local: Union[str, Path], bucket_name: str):
    """
    download function from aws s3.
    Args:
        src_path_in_s3: Union[str, Path]: a path points a path in aws s3 that the file will be download.
        dst_path_in_local: Union[str, Path]: a path points a local path that the file will be saved.
        bucket_name: str: s3 bucket name.
    """
    aws_access_key_id, aws_secret_access_key = get_keys()

    client = boto3.client(
        service_name='s3',
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key)

    # TODO: add error handling(file not found in s3, client initializing error)
    logger.info(f"Start downloading: {dst_path_in_local}")
    client.download_file(bucket_name, src_path_in_s3, dst_path_in_local)
    logger.info(f"File downloaded: {dst_path_in_local}")


@contextmanager
def download_as_temporary(src_path_in_s3: Union[str, Path], bucket_name: str) -> Path:
    """
    This context manager downloads a file from s3 as temporary.

    Args:
        same as the `download` function.
    Returns:
        Path: temporary file path.
    """
    tmp_file_path = tempfile.NamedTemporaryFile().name

    download(src_path_in_s3, tmp_file_path, bucket_name)

    try:
        yield Path(tmp_file_path)

    finally:
        logger.info(f"the temporary file removed: {tmp_file_path}")
        tmp_file_path.close()
