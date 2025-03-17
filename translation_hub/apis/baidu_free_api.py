import time
import urllib.parse

import requests

from translation_hub.api import Api
from translation_hub.core.enums import Languages
from translation_hub import exceptions
import json
from translation_hub.validator_handler import (
    ContentValidatorHandler,
)


class BaiduFreeAPI(Api):
    """
    百度翻译 (无需翻墙,无需秘钥,免费)

    百度翻译随时可能会改变接口，不保证长期可用。目前测试正常。
    使用的时候注意请求频率，不要频繁请求，否则可能会被百度限制。

    Notes:
        免费的百度翻译不支持自动检测语言,请手动指定源语言
    """

    def __init__(self):
        self.content_validator_handler = ContentValidatorHandler()

    api_url: str = "https://fanyi.baidu.com/ait/text/translate"

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

        if source is Languages.Auto:
            raise exceptions.InvalidLanguageError(
                "免费百度翻译不支持自动检测语言,请手动指定源语言"
            )

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36",
            "Accept": "text/event-stream",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Content-Type": "application/json",
            "Pragma": "no-cache",
            "Cache-Control": "no-cache",
            "sec-ch-ua-platform": '"Windows"',
            "sec-ch-ua": '"Chromium";v="134", "Not:A-Brand";v="24", "Google Chrome";v="134"',
            "sec-ch-ua-mobile": "?0",
            "Origin": "https://fanyi.baidu.com",
            "Sec-Fetch-Site": "same-origin",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Dest": "empty",
            "Referer": f"https://fanyi.baidu.com/mtpe-individual/multimodal?query={urllib.parse.quote(text)}&lang={source.value}2{target.value}",
            "Accept-Language": "zh-CN,zh;q=0.9",
        }

        payload = {
            "query": text,
            "from": source.value,
            "to": target.value,
            "reference": "",
            "corpusIds": [],
            "needPhonetic": True,
            "domain": "common",
            "milliTimestamp": int(str(time.time_ns())[:13]),
        }
        try:
            response = requests.post(
                self.api_url, data=json.dumps(payload), headers=headers
            )
            return self.extraxt_translated_text(response.text)
        except requests.RequestException as e:
            raise exceptions.RequestError(str(e)) from e
        except json.JSONDecodeError as e:
            raise exceptions.JsonDecodeError(f"Failed to decode response: {e}")
        except Exception as e:
            raise exceptions.UnknownError(str(e)) from e

    @staticmethod
    def extraxt_translated_text(response: str):
        result = [
            x
            for x in response.splitlines()
            if x.startswith("data: ") and "Translating" in x
        ]
        if len(result) > 0:
            result = result[0].split("data: ")[1]
            return json.loads(result)["data"]["list"][0]["dst"]
        raise exceptions.ResponseError(f"响应错误：没有找到翻译结果: {response}")
