import json
import os

from translation_hub import exceptions
from translation_hub.api import Api
from translation_hub.config import cfg
from translation_hub.core.enums import Languages
from translation_hub.utils.requests import request
from translation_hub.validator_handler import (
    SecretKeyValidatorHandler,
    ContentValidatorHandler,
)
import urllib
import urllib.error
import logging


class DeeplApi(Api):
    """
    Deepl API

    产品说明:
        免费额度: 50万 字/月
        开通地址: https://www.deepl.com/zh/pro-api
        文档地址: https://developers.deepl.com/docs/api-reference

    使用说明:
        deepl 对于中英文翻译的准确度较高，需要注册账号并创建应用获取 API Key。

    正确返回值示例:
        {"translations":[{"detected_source_language":"EN","text":"你好，世界"}]}

    错误返回值示例:
        HTTP 429: too many requests
        HTTP 456: quota exceeded
        HTTP 500: internal server error
    """

    api_url = "https://api-free.deepl.com/v2/translate"

    def __init__(self, api_key: str | None = None):
        self.api_key = self._get_api_id_and_key(api_key)

        self.content_validator_handler = ContentValidatorHandler()
        secret_key_validator_handler = SecretKeyValidatorHandler()
        # 验证 API Key
        is_api_key_valid = secret_key_validator_handler.validate(self.api_key)
        logging.debug(self.api_key)

        if not is_api_key_valid:
            raise exceptions.InvalidSecretKeyError(
                f"Invalid API Key, please check and try again."
                f"current api_key: {self.api_key}"
            )

    def translate(
        self,
        text: str,
        source: Languages | str = Languages.English,
        target: Languages | str = Languages.Chinese,
    ) -> str:
        text = text.strip()

        is_content_valid: bool = self.content_validator_handler.validate(text)
        if not is_content_valid:
            raise exceptions.InvalidContentError(f"Invalid content: {text}")

        source = self._trans_language(source)
        target = self._trans_language(target)

        # deepl 的 API key 是放在 header 的 Authorization 头中的
        headers = {
            "Authorization": f"DeepL-Auth-Key {self.api_key}",
            "Content-Type": "application/json",
        }

        # deepl没有source_lang参数就能自动识别
        if source == "auto":
            json_data = {"text": [text], "target_lang": target}
        else:
            json_data = {"text": [text], "source_lang": source, "target_lang": target}

        try:
            response = request(self.api_url, headers, json_data=json_data)
            logging.debug(f"请求成功: {response}")

        except urllib.error.HTTPError as e:
            match e.code:
                case 403:
                    raise exceptions.RequestError("请求被拒绝: 请检查密钥是否正确")
                case 429:
                    raise exceptions.RequestError("请求次数过多: 请稍后再试")
                case 456:
                    raise exceptions.RequestError("超出配额: 请稍后再试")
                case 500:
                    raise exceptions.ServerError("服务器错误: 请稍后再试")
            raise exceptions.UnknownError(str(e))
        except Exception as e:
            raise exceptions.UnknownError(str(e))

        try:
            response_data = json.loads(response)
            result = response_data["translations"][0]["text"]
        except json.JSONDecodeError as e:
            raise exceptions.JsonDecodeError(f"无法解码 JSON: 不合法的 JSON: {e}")
        except KeyError as e:
            raise exceptions.ResponseError(f"响应错误: {response},错误: {e}")

        return result

    def _trans_language(self, languages: Languages | str) -> str:
        """将语言转换为 Deepl 支持的语言代码"""
        if isinstance(languages, Languages):
            languages = languages.value

        trans_dict: dict[str, str] = {
            "auto": "auto",
            "zh": "ZH",
            "en": "EN",
            "ru": "RU",
            "ja": "JA",
            "kor": "KO",
        }

        return trans_dict.get(languages) or languages

    def _get_api_id_and_key(self, api_key: str | None) -> str:
        """先从环境变量中获取，如果没有则从配置文件中获取"""
        if api_key:
            return api_key

        api_key = os.environ.get("DeeplApiKey")
        if api_key:
            return api_key

        api_key = cfg.get(cfg.DeeplApiKey)
        if api_key:
            return api_key

        raise exceptions.InvalidSecretKeyError(
            f"Invalid API Key, please check and try again."
            f"current api_key: {api_key}"
        )
