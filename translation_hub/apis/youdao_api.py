import hashlib
import json
import os
import time
import uuid
import urllib
import urllib.error

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


class YoudaoApi(Api):
    """
    Youdao 翻译 API

    产品说明:
        免费额度: 新人赠送 50 元, 无后续免费额度,每 100 万字符 48 元
        开通地址: https://ai.youdao.com/product-fanyi-text.s
        文档地址: https://ai.youdao.com/DOCSIRMA/html/trans/api/wbfy/index.html

    使用说明:
        Youdao 翻译没有每月的免费额度，需要充值后才能使用，中英文翻译的准确度较高，有冗余部分，默认会返回翻译结果的发音链接，不能很好的控制。

    正确返回值示例:
        {
          "tSpeakUrl":"https://openapi.youdao.com/ttsapi?q=Hello%2C+world&langType=en-USA&sign=BA31E66617027E90255441CED4DAD187&salt=1733782913720&voice=4&format=mp3&appKey=2e276409e88add8a&ttsVoiceStrict=false&osType=api",
          "requestId":"025cab58-9bba-4726-9ec5-ee6dccfde971",
          "query":"你好,世界",
          "isDomainSupport":false,
          "translation":[
            "Hello, world"
          ],
          "mTerminalDict":{
            "url":"https://m.youdao.com/m/result?lang=zh-CHS&word=%E4%BD%A0%E5%A5%BD%2C%E4%B8%96%E7%95%8C"
          },
          "errorCode":"0",
          "dict":{
            "url":"yddict://m.youdao.com/dict?le=eng&q=%E4%BD%A0%E5%A5%BD%2C%E4%B8%96%E7%95%8C"
          },
          "webdict":{
            "url":"http://mobile.youdao.com/dict?le=eng&q=%E4%BD%A0%E5%A5%BD%2C%E4%B8%96%E7%95%8C"
          },
          "l":"zh-CHS2en",
          "isWord":false,
          "speakUrl":"https://openapi.youdao.com/ttsapi?q=%E4%BD%A0%E5%A5%BD%2C%E4%B8%96%E7%95%8C&langType=zh-CHS&sign=BDDE59DC15C7EF09FADD69BAD437F538&salt=1733782913720&voice=4&format=mp3&appKey=2e276409e88add8a&ttsVoiceStrict=false&osType=api"
        }

    错误返回值示例:
        {"requestId":"1e8dfafb-2605-4061-b807-852dd750892f","errorCode":"108","l":"源语言2目标语言"}
    """

    api_url = "https://openapi.youdao.com/api"
    error_codes = {
        101: "缺少必填的参数,首先确保必填参数齐全，然后确认参数书写是否正确。",
        102: "不支持的语言类型",
        103: "翻译文本过长",
        104: "不支持的API类型",
        105: "不支持的签名类型",
        106: "不支持的响应类型",
        107: "不支持的传输加密类型",
        108: "应用ID无效，注册账号，登录后台创建应用并完成绑定，可获得应用ID和应用密钥等信息",
        109: "batchLog格式不正确",
        110: "无相关服务的有效应用,应用没有绑定服务应用，可以新建服务应用。注：某些服务的翻译结果发音需要tts服务，需要在控制台创建语音合成服务绑定应用后方能使用。",
        111: "开发者账号无效",
        112: "请求服务无效",
        113: "q不能为空",
        114: "不支持的图片传输方式",
        116: "strict字段取值无效，请参考文档填写正确参数值",
        201: "解密失败，可能为DES,BASE64,URLDecode的错误",
        202: "签名检验失败,如果确认应用ID和应用密钥的正确性，仍返回202，一般是编码问题。请确保翻译文本 q 为UTF-8编码.",
        203: "访问IP地址不在可访问IP列表",
        205: "请求的接口与应用的平台类型不一致，确保接入方式（Android SDK、IOS SDK、API）与创建的应用平台类型一致。如有疑问请参考入门指南",
        206: "因为时间戳无效导致签名校验失败",
        207: "重放请求",
        301: "辞典查询失败",
        302: "翻译查询失败",
        303: "服务端的其它异常",
        304: "翻译失败，请联系技术同学",
        308: "rejectFallback参数错误",
        309: "domain参数错误",
        310: "未开通领域翻译服务",
        401: "账户已经欠费，请进行账户充值",
        402: "offlinesdk不可用",
        411: "访问频率受限,请稍后访问",
        412: "长请求过于频繁，请稍后访问",
        1001: "无效的OCR类型",
        1002: "不支持的OCR image类型",
        1003: "不支持的OCR Language类型",
        1004: "识别图片过大",
        1201: "图片base64解密失败",
        1301: "OCR段落识别失败",
        1411: "访问频率受限",
        1412: "超过最大识别字节数",
        2003: "不支持的语言识别Language类型",
        2004: "合成字符过长",
        2005: "不支持的音频文件类型",
        2006: "不支持的发音类型",
        2201: "解密失败",
        2301: "服务的异常",
        2411: "访问频率受限,请稍后访问",
        2412: "超过最大请求字符数",
        3001: "不支持的语音格式",
        3002: "不支持的语音采样率",
        3003: "不支持的语音声道",
        3004: "不支持的语音上传类型",
        3005: "不支持的语言类型",
        3006: "不支持的识别类型",
        3007: "识别音频文件过大",
        3008: "识别音频时长过长",
        3009: "不支持的音频文件类型",
        3010: "不支持的发音类型",
        3201: "解密失败",
        3301: "语音识别失败",
        3302: "语音翻译失败",
        3303: "服务的异常",
        3411: "访问频率受限,请稍后访问",
        3412: "超过最大请求字符数",
        4001: "不支持的语音识别格式",
        4002: "不支持的语音识别采样率",
        4003: "不支持的语音识别声道",
        4004: "不支持的语音上传类型",
        4005: "不支持的语言类型",
        4006: "识别音频文件过大",
        4007: "识别音频时长过长",
        4201: "解密失败",
        4301: "语音识别失败",
        4303: "服务的异常",
        4411: "访问频率受限,请稍后访问",
        4412: "超过最大请求时长",
        5001: "无效的OCR类型",
        5002: "不支持的OCR image类型",
        5003: "不支持的语言类型",
        5004: "识别图片过大",
        5005: "不支持的图片类型",
        5006: "文件为空",
        5201: "解密错误，图片base64解密失败",
        5301: "OCR段落识别失败",
        5411: "访问频率受限",
        5412: "超过最大识别流量",
        9001: "不支持的语音格式",
        9002: "不支持的语音采样率",
        9003: "不支持的语音声道",
        9004: "不支持的语音上传类型",
        9005: "不支持的语音识别 Language类型",
        9301: "ASR识别失败",
        9303: "服务器内部错误",
        9411: "访问频率受限（超过最大调用次数）",
        9412: "超过最大处理语音长度",
        10001: "无效的OCR类型",
        10002: "不支持的OCR image类型",
        10004: "识别图片过大",
        10201: "图片base64解密失败",
        10301: "OCR段落识别失败",
        10411: "访问频率受限",
        10412: "超过最大识别流量",
        11001: "不支持的语音识别格式",
        11002: "不支持的语音识别采样率",
        11003: "不支持的语音识别声道",
        11004: "不支持的语音上传类型",
        11005: "不支持的语言类型",
        11006: "识别音频文件过大",
        11007: "识别音频时长过长，最大支持30s",
        11201: "解密失败",
        11301: "语音识别失败",
        11303: "服务的异常",
        11411: "访问频率受限,请稍后访问",
        11412: "超过最大请求时长",
        12001: "图片尺寸过大",
        12002: "图片base64解密失败",
        12003: "引擎服务器返回错误",
        12004: "图片为空",
        12005: "不支持的识别图片类型",
        12006: "图片无匹配结果",
        13001: "不支持的角度类型",
        13002: "不支持的文件类型",
        13003: "表格识别图片过大",
        13004: "文件为空",
        13301: "表格识别失败",
        15001: "需要图片",
        15002: "图片过大（1M）",
        15003: "服务调用失败",
        17001: "需要图片",
        17002: "图片过大（1M）",
        17003: "识别类型未找到",
        17004: "不支持的识别类型",
        17005: "服务调用失败",
    }

    def __init__(self, api_id: str | None = None, api_key: str | None = None):
        self.api_id, self.api_key = self._get_api_id_and_key(api_id, api_key)

        self.content_validator_handler = ContentValidatorHandler()
        secret_key_validator_handler = SecretKeyValidatorHandler()
        # 验证 API Key
        is_api_key_valid = secret_key_validator_handler.validate(self.api_key)

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

        def encrypt(sign_str):
            hash_algorithm = hashlib.sha256()
            hash_algorithm.update(sign_str.encode("utf-8"))
            return hash_algorithm.hexdigest()

        def truncate(q):
            if q is None:
                return None
            size = len(q)
            return q if size <= 20 else q[0:10] + str(size) + q[size - 10 : size]

        def do_request(data):
            headers = {"Content-Type": "application/x-www-form-urlencoded"}
            return request(self.api_url, data=data, headers=headers)

        data = {"from": source, "to": target, "signType": "v3"}
        current_time = str(int(time.time()))
        data["curtime"] = current_time
        salt = str(uuid.uuid1())
        sign_str = self.api_id + truncate(text) + salt + current_time + self.api_key
        sign = encrypt(sign_str)
        data["appKey"] = self.api_id
        data["q"] = text
        data["salt"] = salt
        data["sign"] = sign

        try:
            response = do_request(data)
            logging.debug(f"请求成功: {response}")
        except urllib.error.HTTPError as e:
            raise exceptions.RequestError(f"网络请求错误: {e}")
        except Exception as e:
            raise exceptions.UnknownError(f"未知错误: {e}")

        try:
            response_data = json.loads(response)
            if response_data["errorCode"] != "0":
                error_code = response_data["errorCode"]
                error_msg = self.error_codes.get(int(error_code), "未知错误")
                raise exceptions.RequestError(f"请求错误: {error_msg}")
            result = response_data["translation"][0]

        except json.JSONDecodeError as e:
            raise exceptions.JsonDecodeError(f"Failed to decode response: {e}")
        except KeyError as e:
            raise exceptions.JsonDecodeError(f"Failed to decode response: {e}")

        return result

    def _trans_language(self, languages: Languages | str) -> str:
        """将语言转换为 Deepl 支持的语言代码"""
        if isinstance(languages, Languages):
            languages = languages.value

        trans_dict: dict[str, str] = {
            "auto": "auto",
            "zh": "zh-CHS",
            "en": "en",
            "ru": "ru",
            "ja": "ja",
            "kor": "ko",
        }

        return trans_dict.get(languages) or languages

    def _get_api_id_and_key(
        self, api_id: str | None, api_key: str | None
    ) -> tuple[str, str]:
        """先从环境变量中获取，如果没有则从配置文件中获取"""
        if api_id and api_key:
            return api_id, api_key

        api_id = os.environ.get("YoudaoAppId")
        api_key = os.environ.get("YoudaoSecretKey")
        if api_id and api_key:
            return api_id, api_key

        api_id = cfg.get(cfg.YoudaoAppId)
        api_key = cfg.get(cfg.YoudaoSecretKey)
        if api_id and api_key:
            return api_id, api_key

        raise exceptions.InvalidSecretKeyError(
            f"Invalid API ID or API Key, please check and try again."
            f"current api_id: {api_id}, current api_key: {api_key}"
        )
