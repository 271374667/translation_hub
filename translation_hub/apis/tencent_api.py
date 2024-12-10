import hashlib
import hmac
import json
import os
import time

from translation_hub import exceptions
from translation_hub.api import Api
from translation_hub.config import cfg
from translation_hub.core.enums import Languages
from translation_hub.validator_handler import (
    SecretKeyValidatorHandler,
    ContentValidatorHandler,
)
import urllib
import urllib.error
import urllib.request
import logging


class TencentApi(Api):
    """
    腾讯翻译 API

    产品说明:
        免费额度: 500万 字/月
        开通地址: https://console.cloud.tencent.com/cam/capi
        文档地址: https://cloud.tencent.com/document/product/551

    使用说明:
        腾讯财大气粗,每月免费额度高达 500 万字,appid 和 secretkey 需要在腾讯云控制台申请
        教程: https://cloud.tencent.com.cn/developer/information/腾讯翻译api申请教程-article

    正确返回值示例:
        {
            "Response": {
                "RequestId": "5a94cad9-48e3-4318-b57e-2f7c59c83929",
                "Source": "zh",
                "Target": "en",
                "TargetText": "Hello world!",
                "UsedAmount": 6
            }
        }

    错误返回值示例:
        {
            "Response": {
                "Error": {
                    "Code": "AuthFailure.SecretIdNotFound",
                    "Message": "The SecretId is not found, please ensure that your SecretId is correct."
                },
                "RequestId": "f93b6a33-9a12-46cc-bb19-46c086a21ec6"
            }
        }
    """

    api_url = "https://tmt.tencentcloudapi.com/"

    def __init__(self, api_id: str | None = None, api_key: str | None = None):
        self.api_id, self.api_key = self._get_api_id_and_key(api_id, api_key)

        self.content_validator_handler = ContentValidatorHandler()
        secret_key_validator_handler = SecretKeyValidatorHandler()
        # 验证 API ID 和 API Key
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
        """
        调用腾讯翻译 API 进行翻译。

        参数:
            text (str): 待翻译的文本。
            source (Languages, optional): 源语言，默认为英语。
            target (Languages, optional): 目标语言，默认为中文。

        返回:
            str: 翻译后的文本。
        """
        # 将语言转换为腾讯翻译 API 支持的语言代码
        text = text.strip()

        is_content_valid: bool = self.content_validator_handler.validate(text)
        if not is_content_valid:
            raise exceptions.InvalidContentError(f"Invalid content: {text}")

        source = self._trans_language(source)
        target = self._trans_language(target)

        # 腾讯的API非常麻烦，看得出非常想让别人去用它那个庞大的 SDK

        # 构造请求参数
        payload = {
            "SourceText": text,
            "Source": source,
            "Target": target,
            "ProjectId": 0,
        }

        # 构造请求头
        timestamp = int(time.time())
        headers = {
            "Authorization": self._get_authorization(payload, timestamp),
            "Content-Type": "application/json; charset=utf-8",
            "Host": "tmt.tencentcloudapi.com",
            "X-TC-Action": "TextTranslate",
            "X-TC-Version": "2018-03-21",
            "X-TC-Timestamp": str(timestamp),
            "X-TC-Region": "ap-guangzhou",
        }

        try:
            request_data = json.dumps(payload).encode("utf-8")
            req = urllib.request.Request(
                self.api_url, data=request_data, headers=headers, method="POST"
            )
            with urllib.request.urlopen(req) as response:
                response = response.read().decode("utf-8")
            logging.debug(f"请求成功: {response}")
        except urllib.error.HTTPError as e:
            raise exceptions.RequestError(str(e))
        except Exception as e:
            raise exceptions.UnknownError(str(e))

        try:
            response_data = json.loads(response)
            if "Error" in response_data["Response"]:
                raise exceptions.ServerError(
                    f"服务出现错误: {response_data['Response']['Error']}"
                )
            return response_data["Response"]["TargetText"]
        except json.JSONDecodeError as e:
            raise exceptions.JsonDecodeError(f"Failed to decode response: {e}")
        except KeyError as e:
            raise exceptions.ResponseError(f"Response error: {response}, error: {e}")

    def _trans_language(self, languages: Languages | str) -> str:
        """转换语言代码为支持的格式"""
        if isinstance(languages, Languages):
            languages = languages.value

        trans_dict: dict[str, str] = {
            "auto": "auto",
            "zh": "zh",
            "en": "en",
            "ru": "ru",
            "ja": "ja",
            "kor": "ko",
        }

        return trans_dict.get(languages) or languages

    def _get_api_id_and_key(
        self, api_id: str | None = None, api_key: str | None = None
    ) -> tuple[str, str]:
        """先从环境变量中获取，如果没有则从配置文件中获取"""
        if api_id and api_key:
            return api_id, api_key

        api_id = os.environ.get("TencentAppId")
        api_key = os.environ.get("TencentSecretKey")
        if api_id and api_key:
            return api_id, api_key

        api_id = cfg.get(cfg.TencentAppId)
        api_key = cfg.get(cfg.TencentSecretKey)
        if api_id and api_key:
            return api_id, api_key

        raise exceptions.InvalidSecretKeyError(
            f"Invalid API ID or API Key, please check and try again."
            f"current api_id: {api_id}, current api_key: {api_key}"
        )

    def _get_authorization(self, payload: dict, timestamp: int) -> str:
        """获取请求头中的 Authorization 字段"""
        # 公共参数
        host = "tmt.tencentcloudapi.com"
        service = "tmt"
        algorithm = "TC3-HMAC-SHA256"
        date = time.strftime("%Y-%m-%d", time.gmtime(timestamp))

        # ************* 步骤 1：拼接规范请求串 *************
        http_request_method = "POST"
        canonical_uri = "/"
        canonical_querystring = ""
        canonical_headers = (
            "content-type:application/json; charset=utf-8\nhost:" + host + "\n"
        )
        signed_headers = "content-type;host"
        hashed_request_payload = hashlib.sha256(
            json.dumps(payload).encode("utf-8")
        ).hexdigest()
        canonical_request = (
            http_request_method
            + "\n"
            + canonical_uri
            + "\n"
            + canonical_querystring
            + "\n"
            + canonical_headers
            + "\n"
            + signed_headers
            + "\n"
            + hashed_request_payload
        )

        # ************* 步骤 2：拼接待签名字符串 *************
        credential_scope = date + "/" + service + "/tc3_request"
        hashed_canonical_request = hashlib.sha256(
            canonical_request.encode("utf-8")
        ).hexdigest()
        string_to_sign = (
            algorithm
            + "\n"
            + str(timestamp)
            + "\n"
            + credential_scope
            + "\n"
            + hashed_canonical_request
        )

        # ************* 步骤 3：计算签名 *************
        def sign(key, msg):
            return hmac.new(key, msg.encode("utf-8"), hashlib.sha256).digest()

        secret_date = sign(("TC3" + self.api_key).encode("utf-8"), date)
        secret_service = sign(secret_date, service)
        secret_signing = sign(secret_service, "tc3_request")
        signature = hmac.new(
            secret_signing, string_to_sign.encode("utf-8"), hashlib.sha256
        ).hexdigest()

        # ************* 步骤 4：构造 Authorization 头部 *************
        authorization = (
            algorithm
            + " "
            + "Credential="
            + self.api_id
            + "/"
            + credential_scope
            + ", "
            + "SignedHeaders="
            + signed_headers
            + ", "
            + "Signature="
            + signature
        )

        return authorization
