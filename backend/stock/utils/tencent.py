from application import dispatch
from qcloud_cos import CosConfig
from qcloud_cos import CosS3Client


class Tencent():

    def __init__(self) -> None:
        self.secret_id = dispatch.get_system_config_values("tencentcloud.secret_id")
        self.secret_key = dispatch.get_system_config_values("tencentcloud.secret_key")

    def get_cos_client(self):
        config = CosConfig(Region="ap-shanghai", SecretId=self.secret_id, SecretKey=self.secret_key)
        return CosS3Client(config)
