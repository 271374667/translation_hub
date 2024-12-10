from translation_hub.api import Api
from translation_hub.core.enums import Languages
from translation_hub.utils.requests import request
from translation_hub import exceptions
from hashlib import md5
import random
import json
import logging
from translation_hub.validator_handler import (
    SecretKeyValidatorHandler,
    ContentValidatorHandler,
)
import os
from translation_hub.config import cfg


class BaiduAPI(Api):
    """
    百度翻译 API

    产品说明:
        免费额度: 200万 字/月
        开通地址: https://api.fanyi.baidu.com/product/11
        文档地址: https://api.fanyi.baidu.com/doc/21

    使用说明:
        百度翻译 API 通过百度翻译开放平台提供，需要注册账号并创建应用获取 API ID 和 API Key。

    正确返回值示例:
        {'from': 'en', 'to': 'zh', 'trans_result': [{'src': 'Hello', 'dst': '你好'}]}

    错误返回值示例:
        {"error_code":"54001","error_msg":"Invalid Sign"}
    """

    api_url: str = "http://api.fanyi.baidu.com/api/trans/vip/translate"

    def __init__(self, api_id: str | None = None, api_key: str | None = None):
        self.api_id, self.api_key = self._get_api_id_and_key(api_id, api_key)

        # 验证 API ID 和 API Key
        self.content_validator_handler = ContentValidatorHandler()
        self.secret_key_validator_handler = SecretKeyValidatorHandler()
        is_api_id_valid: bool = self.secret_key_validator_handler.validate(self.api_id)
        is_api_key_valid: bool = self.secret_key_validator_handler.validate(
            self.api_key
        )

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
        text = text.strip()
        is_content_valid: bool = self.content_validator_handler.validate(text)
        if not is_content_valid:
            raise exceptions.InvalidContentError(f"Invalid content: {text}")

        if isinstance(source, Languages):
            source = source.value
        if isinstance(target, Languages):
            target = target.value

        salt = random.randint(32768, 65536)

        sign = md5(f"{self.api_id}{text}{salt}{self.api_key}".encode()).hexdigest()

        payload = {
            "appid": self.api_id,
            "q": text,
            "from": source,
            "to": target,
            "salt": salt,
            "sign": sign,
        }

        headers = {"Content-Type": "application/x-www-form-urlencoded"}

        try:
            response = request(self.api_url, headers, payload=payload)
            response_data = json.loads(response)
            logging.debug(f"请求成功: {response_data}")
        except json.JSONDecodeError as e:
            raise exceptions.JsonDecodeError(f"Failed to decode response: {e}")
        except Exception as e:
            raise exceptions.RequestError(str(e))

        if "error_code" in response_data:
            error_code = response_data["error_code"]
            error_msg = response_data.get("error_msg", "Unknown error")

            match error_code:
                case "52001":
                    raise exceptions.ServerError(
                        "请求超时: 检查请求query是否超长，以及原文或译文参数是否在支持的语种列表里"
                    )
                case "52002":
                    raise exceptions.ServerError("服务器系统错误: 请重试")
                case "52003":
                    raise exceptions.ServerError(
                        "未授权用户: 请检查appid是否正确或者服务是否开通"
                    )
                case "54000":
                    raise exceptions.ServerError("必填参数为空: 请检查是否少传参数")
                case "54001":
                    raise exceptions.ServerError("签名错误: 请检查您的签名生成方法")
                case "54003":
                    raise exceptions.ServerError(
                        "访问频率受限: 请降低您的调用频率，或在控制台进行身份认证后切换为高级版/尊享版"
                    )
                case "54004":
                    raise exceptions.ServerError(
                        "账户余额不足: 请前往管理控制台为账户充值"
                    )
                case "54005":
                    raise exceptions.ServerError(
                        "长query请求频繁: 请降低长query的发送频率，3s后再试"
                    )
                case "58000":
                    raise exceptions.ServerError(
                        "客户端IP非法: 检查个人资料里填写的IP地址是否正确，可前往开发者信息-基本信息修改"
                    )
                case "58001":
                    raise exceptions.ServerError(
                        "译文语言方向不支持: 检查译文语言是否在语言列表里"
                    )
                case "58002":
                    raise exceptions.ServerError(
                        "服务当前已关闭: 请前往管理控制台开启服务"
                    )
                case "58003":
                    raise exceptions.ServerError(
                        "此IP已被封禁: 同一IP当日使用多个APPID发送翻译请求，则该IP将被封禁当日请求权限，次日解封。请勿将APPID和密钥填写到第三方软件中。"
                    )
                case "90107":
                    raise exceptions.ServerError(
                        "认证未通过或未生效: 请前往我的认证查看认证进度"
                    )
                case "20003":
                    raise exceptions.ServerError("请求内容存在安全风险: 请检查请求内容")
                case _:
                    raise exceptions.UnknownError(
                        f"Error code: {error_code}, message: {error_msg}"
                    )

        try:
            result = response_data["trans_result"][0]["dst"]
        except KeyError:
            raise exceptions.ResponseError(f"Failed to get translation: {response}")
        except Exception as e:
            raise exceptions.UnknownError(str(e))
        return result

    def _get_api_id_and_key(
        self, api_id: str | None, api_key: str | None
    ) -> tuple[str, str]:
        """先从环境变量中获取，如果没有则从配置文件中获取"""
        if api_id and api_key:
            return api_id, api_key

        api_id = os.environ.get("BaiduAppId")
        api_key = os.environ.get("BaiduSecretKey")
        if api_id and api_key:
            return api_id, api_key

        api_id = cfg.get(cfg.BaiduAppId)
        api_key = cfg.get(cfg.BaiduSecretKey)
        if api_id and api_key:
            return api_id, api_key

        raise exceptions.InvalidSecretKeyError(
            f"Invalid API ID or API Key, please check and try again."
            f"current api_id: {api_id}, current api_key: {api_key}"
        )
