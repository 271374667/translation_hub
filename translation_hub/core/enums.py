from enum import Enum


class Languages(Enum):
    Auto = "auto"  # 自动检测(需要目标API支持, translatehub不提供检测)
    Chinese = "zh"  # 中文
    English = "en"  # 英文
    Russia = "ru"  # 俄文
    Japanese = "ja"  # 日文
    Korea = "kor"  # 韩文
