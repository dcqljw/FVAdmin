import os.path
import hashlib
from io import BytesIO

import boto3
from botocore.client import Config

from core.settings import settings


class OssClient:
    def __init__(self):
        self.client = boto3.client(
            's3',
            endpoint_url=settings.OSS_URL,
            aws_access_key_id=settings.OSS_KEY,
            aws_secret_access_key=settings.OSS_SECRET,
            config=Config(signature_version='s3v4'),
            region_name='ap-southeast-1'
        )

    def get_md5(self, data):
        return hashlib.md5(data).hexdigest()

    def upload_file(self, file_path):
        file_name = os.path.basename(file_path)
        print(file_name)
        self.client.upload_file(file_path, settings.OSS_BUCKET, file_name)

    def upload_file_by_stream(self, file, file_name, extra_args=None):
        file.seek(0)
        self.client.upload_fileobj(file, settings.OSS_BUCKET, file_name, extra_args)


oss_client = OssClient()

if __name__ == '__main__':
    oss_client.upload_file(r"D:\code\RPAEngine\packages\numpy-1.24.4-cp38-cp38-win_amd64.whl")
