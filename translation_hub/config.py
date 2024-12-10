from translation_hub.utils.config import QConfig, ConfigItem, qconfig
from translation_hub.core.paths import CONFIG_FILE
import logging


class Config(QConfig):
    BaiduAppId = ConfigItem("Baidu", "BaiduAppId", "")
    BaiduSecretKey = ConfigItem("Baidu", "BaiduSecretKey", "")
    DeeplApiKey = ConfigItem("Deepl", "DeeplApiKey", "")
    YoudaoAppId = ConfigItem("Youdao", "YoudaoAppId", "")
    YoudaoSecretKey = ConfigItem("Youdao", "YoudaoSecretKey", "")
    TencentAppId = ConfigItem("Tencent", "TencentAppId", "")
    TencentSecretKey = ConfigItem("Tencent", "TencentSecretKey", "")
    AliyunAppId = ConfigItem("Aliyun", "AliyunAppId", "")
    AliyunSecretKey = ConfigItem("Aliyun", "AliyunSecretKey", "")


cfg = Config()
cfg.file = CONFIG_FILE
if not CONFIG_FILE.exists():
    cfg.save()
    logging.info(f"Config file not found, create a new one at {CONFIG_FILE}")
qconfig.load(CONFIG_FILE, cfg)
