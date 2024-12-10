import logging
from translation_hub.apis.google_api import GoogleApi
from translation_hub.apis.aliyun_api import AliyunApi
from translation_hub.apis.baidu_api import BaiduAPI
from translation_hub.apis.tencent_api import TencentApi
from translation_hub.apis.youdao_api import YoudaoApi
from translation_hub.apis.deepl_api import DeeplApi
from translation_hub.core.enums import Languages

__all__ = [
    "GoogleApi",
    "AliyunApi",
    "BaiduAPI",
    "TencentApi",
    "YoudaoApi",
    "DeeplApi",
    Languages,
]

logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s"
)
