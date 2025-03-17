import json

import requests

from translation_hub import exceptions
from translation_hub.api import Api
import re
from translation_hub.core.enums import Languages
from translation_hub.validator_handler import (
    ContentValidatorHandler,
)
import logging


class BingFreeApi(Api):
    """
    Bing翻译 API(无需秘钥,免费)

    Bing翻译随时可能会改变接口，不保证长期可用。目前测试正常。
    使用的时候注意请求频率，不要频繁请求，否则可能会被Bing限制。
    """

    api_url: str = "https://www.bing.com/ttranslatev3"
    host_url: str = "https://cn.bing.com/translator"
    iid_regex: str = r'data-iid="([^"]+)"'
    ig_regex: str = r'IG:"(\w+)"'
    token_regex: str = r'var params_AbusePreventionHelper = \[(\d+),"([^"]+)",\d+\];'

    def __init__(self):
        self.content_validator_handler = ContentValidatorHandler()
        self._session = requests.Session()

        self._headers = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36 Edg/129.0.0.0"
        }
        self._data: dict | None = None  # 通过第一次请求获取到的参数
        self._data_iid: str | None = None  # 通过第一次请求获取到的参数
        self._ig: str | None = None  # 通过第一次请求获取到的参数

    def translate(
        self,
        text: str,
        source: Languages | str = Languages.Auto,
        target: Languages | str = Languages.Chinese,
    ) -> str:
        text: str = text.strip()

        is_content_valid: bool = self.content_validator_handler.validate(text)
        if not is_content_valid:
            raise exceptions.InvalidContentError(f"Invalid content: {text}")

        source: str = self._trans_language(source)
        target: str = self._trans_language(target)

        # 该方法来自 https://blog.csdn.net/whale_cat/article/details/143622024
        if not self._data:
            self._data = self._get_payload(source, target)
        self._data["text"] = text
        self._data["fromLang"] = source
        self._data["to"] = target

        params: dict = {
            "isVertical": "1",
            "IG": self._ig,
            "IID": self._data_iid,
        }

        try:
            response = self._session.post(
                self.api_url, data=self._data, headers=self._headers, params=params
            )
            result = response.json()[0]["translations"][0]["text"]
            if not result:
                raise exceptions.ResponseError("Empty response")
            return result
        except requests.RequestException as e:
            raise exceptions.RequestError(str(e)) from e
        except KeyError as e:
            raise exceptions.ResponseError(f"KeyError: {e}")
        except json.JSONDecodeError as e:
            raise exceptions.JsonDecodeError(f"Failed to decode response: {e}")
        except Exception as e:
            raise exceptions.UnknownError(str(e)) from e

    def _trans_language(self, language: Languages | str) -> str:
        """转换语言代码为支持的格式"""
        if isinstance(language, Languages):
            language = language.value

        trans_dict = {
            "auto": "auto-detect",
            "zh": "zh-Hans",
            "en": "en",
            "ja": "ja",
            "kor": "ko",
            "ru": "ru",
        }
        return trans_dict.get(language) or language

    def _get_payload(self, source: str, target: str) -> dict:
        # 先请求一次网站获取到请求头
        try:
            response = self._session.get(self.host_url, headers=self._headers)
            html = response.text
            # 获取data-iid
            self._data_iid = re.search(self.iid_regex, html).group(1)
            # 获取IG
            self._ig = re.search(self.ig_regex, html).group(1)
            # 获取token
            token = re.findall(self.token_regex, html)

            logging.debug(f"data_iid: {self._data_iid}, ig: {self._ig}, token: {token}")

            data = {
                "fromLang": source,
                "to": target,
                "token": token[0][1],
                "key": token[0][0],
                "text": "",
                "tryFetchingGenderDebiasedTranslations": "true",
            }
            return data
        except Exception as e:
            raise exceptions.RequestError(
                f"There are something wrong with the network: {e}"
            )
