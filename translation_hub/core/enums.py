from enum import Enum


class Languages(Enum):
    AUTO = "auto"  # 自动检测(需要目标API支持, translatehub不提供检测)
    CHINESE = "zh"  # 中文
    ENGLISH = "en"  # 英文
    RUSSIA = "ru"  # 俄文
    Japanese = "ja"  # 日文
    Korea = "kor"  # 韩文
