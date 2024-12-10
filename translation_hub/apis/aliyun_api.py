import hashlib
import hmac
import json
import os
import base64
import time
import urllib.parse

from translation_hub import exceptions
from translation_hub.api import Api
from translation_hub.config import cfg
from translation_hub.core.enums import Languages
from translation_hub.utils.requests import request
from translation_hub.validator_handler import (
    SecretKeyValidatorHandler,
    ContentValidatorHandler,
)
import logging
from typing import Literal


class AliyunApi(Api):
    """
    阿里云翻译 API

    产品说明:
        免费额度: 100万 字/月
        开通地址: https://www.aliyun.com/product/ai/alimt
        文档地址: https://help.aliyun.com/zh/machine-translation/

    使用说明:
        阿里云的app_id和app_key注册也比较麻烦，请参考: https://help.aliyun.com/zh/ram/user-guide/create-an-accesskey-pair

    正确返回值示例:
        {
            "RequestId": "F3D8EEF0-1474-53B9-A3BB-E10D6F696D3D",
            "Data": {
                "WordCount": "13",
                "Translated": "你好，世界!"
            },
            "Code": "200"
        }


    错误返回值示例:
        {
            "Message": "语种拼写错误",
            "RequestId": "5605A851-C90E-57B5-A002-47AFEF3F961F",
            "Code": "10033"
        }
    """

    api_url = "http://mt.cn-hangzhou.aliyuncs.com/"

    def __init__(
        self,
        api_id: str | None = None,
        api_key: str | None = None,
        version: Literal["normal", "pro"] = "normal",
    ):
        """
        初始化阿里云翻译 API
        Args:
            api_id: 阿里云API ID
            api_key: 阿里云API Key
            version: 翻译版本，normal: 通用翻译，pro: 专业版翻译(需要额外开通)
        """
        self.version = version
        self.api_id, self.api_key = self._get_api_id_and_key(api_id, api_key)

        self.content_validator_handler = ContentValidatorHandler()
        secret_key_validator_handler = SecretKeyValidatorHandler()

        is_api_id_valid = secret_key_validator_handler.validate(self.api_id)
        is_api_key_valid = secret_key_validator_handler.validate(self.api_key)

        if not is_api_id_valid or not is_api_key_valid:
            raise exceptions.InvalidSecretKeyError(
                f"Invalid API ID or API Key, please check and try again."
                f"current api_id: {self.api_id}, current api_key: {self.api_key}"
            )

    def translate(
        self,
        text: str,
        source: Languages | str = Languages.English,
        target: Languages | str = Languages.Chinese,
    ) -> str:
        """执行翻译请求"""
        text = text.strip()

        is_content_valid: bool = self.content_validator_handler.validate(text)
        if not is_content_valid:
            raise exceptions.InvalidContentError(f"Invalid content: {text}")

        source = self._trans_language(source)
        target = self._trans_language(target)

        # 构造参数
        parameters = {
            "Action": "TranslateGeneral",
            "FormatType": "text",
            "SourceLanguage": source,
            "TargetLanguage": target,
            "SourceText": text,
            "Scene": "general" if self.version == "normal" else "ecommerce",
            "Format": "JSON",
            "Version": "2018-10-12",
            "AccessKeyId": self.api_id,
            "SignatureMethod": "HMAC-SHA1",
            "Timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "SignatureVersion": "1.0",
            "SignatureNonce": str(int(time.time() * 1000)),
            "RegionId": "cn-hangzhou",
        }

        # 计算签名
        parameters["Signature"] = self._calculate_signature(parameters)

        try:
            response = request(url=self.api_url, headers={}, payload=parameters)
            logging.debug(f"请求成功: {response}")
            response_data = json.loads(response)

            if "Code" in response_data and response_data["Code"] != "200":
                error_code = response_data.get("Code")
                error_msg = response_data.get("Message", "Unknown error")
                raise exceptions.ServerError(f"服务器错误: {error_code} - {error_msg}")

        except json.JSONDecodeError as e:
            raise exceptions.JsonDecodeError(f"解析响应失败: {e}")

        try:
            result = response_data["Data"]["Translated"]
            return result
        except KeyError:
            raise exceptions.ResponseError(f"获取翻译结果失败: {response_data}")

    def _trans_language(self, language: Languages | str) -> str:
        """转换语言代码为阿里云支持的格式"""
        if isinstance(language, Languages):
            language = language.value

        trans_dict = {
            "auto": "auto",
            "zh": "zh",
            "en": "en",
            "ja": "ja",
            "kor": "ko",
            "ru": "ru",
        }
        return trans_dict.get(language) or language

    def _get_api_id_and_key(
        self, api_id: str | None, api_key: str | None
    ) -> tuple[str, str]:
        """获取 API ID 和 Key"""
        if api_id and api_key:
            return api_id, api_key

        api_id = os.environ.get("AliyunAppId")
        api_key = os.environ.get("AliyunSecretKey")
        if api_id and api_key:
            return api_id, api_key

        api_id = cfg.get(cfg.AliyunAppId)
        api_key = cfg.get(cfg.AliyunSecretKey)
        if api_id and api_key:
            return api_id, api_key

        raise exceptions.InvalidSecretKeyError(
            f"Invalid API ID or API Key, please check and try again."
            f"current api_id: {api_id}, current api_key: {api_key}"
        )

    def _calculate_signature(self, parameters: dict) -> str:
        """计算阿里云API签名"""
        sorted_params = sorted(parameters.items())
        canonicalized_query = "&".join(
            [f"{self._encode(k)}={self._encode(v)}" for k, v in sorted_params]
        )

        string_to_sign = "GET&%2F&" + self._encode(canonicalized_query)

        h = hmac.new(
            f"{self.api_key}&".encode("utf-8"),
            string_to_sign.encode("utf-8"),
            hashlib.sha1,
        )
        return base64.b64encode(h.digest()).decode()

    def _encode(self, value: str) -> str:
        """URL编码"""
        return (
            urllib.parse.quote(str(value), safe="~")
            .replace("+", "%20")
            .replace("*", "%2A")
            .replace("%7E", "~")
        )
