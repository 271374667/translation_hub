import hashlib
import json
import time
import urllib.error
import uuid

import requests

from translation_hub import exceptions
from translation_hub.api import Api
from translation_hub.core.enums import Languages
from translation_hub.validator_handler import (
    ContentValidatorHandler,
)


class SoGouFreeApi(Api):
    """
    搜狗翻译 API(无需秘钥,免费)

    搜狗翻译随时可能会改变接口，不保证长期可用。目前测试正常。
    使用的时候注意请求频率，不要频繁请求，否则可能会被搜狗限制。
    """

    api_url = "https://fanyi.sogou.com/api/transpc/text/result"

    def __init__(self):
        self.content_validator_handler = ContentValidatorHandler()

    def translate(
        self,
        text: str,
        source: Languages | str = Languages.English,
        target: Languages | str = Languages.Chinese,
    ) -> str:
        text: str = text.strip()

        is_content_valid: bool = self.content_validator_handler.validate(text)
        if not is_content_valid:
            raise exceptions.InvalidContentError(f"Invalid content: {text}")

        source: str = self._trans_language(source)
        target: str = self._trans_language(target)

        # 该方法来自 https://blog.csdn.net/tsk2642014359/article/details/144545180
        payload = {
            "from": source,
            "to": target,
            "text": text,
            "client": "pc",
            "fr": "browser_pc",
            "needQc": 1,
            "s": self.generate_s(source, target, text),
            "uuid": str(uuid.uuid4()),
            "exchange": False,
        }

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36",
            "Accept": "application/json, text/plain, */*",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Content-Type": "application/json",
            "sec-ch-ua-platform": '"Windows"',
            "sec-ch-ua": '"Chromium";v="134", "Not:A-Brand";v="24", "Google Chrome";v="134"',
            "Content-Type": "application/json;charset=UTF-8",
            "sec-ch-ua-mobile": "?0",
            "Origin": "https://fanyi.sogou.com",
            "Sec-Fetch-Site": "same-origin",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Dest": "empty",
            "Referer": "https://fanyi.sogou.com/text",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Cookie": f"ABTEST=8|{time.time()}|v17; SNUID=6259AF050E0B3D940B3A36150E649821; SUID=6C54A20B1F50A20B0000000067D92384; wuid={str(time.time_ns())[:13]}; FQV=ac2545d883b60ad25c12556fab851bd7; translate.sess=c6d99490-d1ca-4159-bb53-d403c04400d1; SUV={str(time.time_ns())[:13]}; SGINPUT_UPSCREEN={str(time.time_ns())[:13]}",
        }

        try:
            response = requests.post(
                self.api_url, data=json.dumps(payload), headers=headers
            )
            return response.json()["data"]["translate"]["dit"]
        except urllib.error.HTTPError as e:
            raise exceptions.RequestError(str(e)) from e
        except urllib.error.URLError as e:
            raise exceptions.RequestError(str(e)) from e
        except json.JSONDecodeError as e:
            raise exceptions.JsonDecodeError(f"Failed to decode response: {e}")
        except Exception as e:
            raise exceptions.UnknownError(str(e)) from e

    @staticmethod
    def generate_s(source: str, target: str, text: str) -> str:
        # 生成 s 参数
        return hashlib.md5(f"{source}{target}{text}109984457".encode()).hexdigest()

    def _trans_language(self, language: Languages | str) -> str:
        """转换语言代码为支持的格式"""
        if isinstance(language, Languages):
            language = language.value

        trans_dict = {
            "auto": "auto",
            "zh": "zh-CHS",
            "en": "en",
            "ja": "ja",
            "kor": "ko",
            "ru": "ru",
        }
        return trans_dict.get(language) or language
