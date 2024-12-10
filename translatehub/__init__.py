import logging
from translatehub.apis.google_api import GoogleApi
from translatehub.apis.aliyun_api import AliyunApi
from translatehub.apis.baidu_api import BaiduAPI
from translatehub.apis.tencent_api import TencentApi
from translatehub.apis.youdao_api import YoudaoApi
from translatehub.core.enums import Languages

__all__ = [
    "GoogleApi",
    "AliyunApi",
    "BaiduAPI",
    "TencentApi",
    "YoudaoApi",
    Languages,
]

logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s"
)
