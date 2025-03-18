import logging
from translation_hub.apis.google_free_api import GoogleFreeApi
from translation_hub.apis.sogou_free_api import SoGouFreeApi
from translation_hub.apis.bing_free_api import BingFreeApi
from translation_hub.apis.baidu_free_api import BaiduFreeAPI
from translation_hub.apis.aliyun_api import AliyunApi
from translation_hub.apis.baidu_api import BaiduApi
from translation_hub.apis.tencent_api import TencentApi
from translation_hub.apis.youdao_api import YoudaoApi
from translation_hub.apis.deepl_api import DeeplApi
from translation_hub.core.enums import Languages

__all__ = [
    "GoogleFreeApi",
    "SoGouFreeApi",
    "BingFreeApi",
    "BaiduFreeAPI",
    "AliyunApi",
    "BaiduApi",
    "TencentApi",
    "YoudaoApi",
    "DeeplApi",
    Languages,
]

logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s"
)
