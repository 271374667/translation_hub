from translation_hub import exceptions
from translation_hub.api import Api
import re
import html
from urllib import parse
from urllib import request
import urllib.error
from translation_hub.core.enums import Languages
from translation_hub.validator_handler import (
    ContentValidatorHandler,
)


class GoogleApi(Api):
    """
    谷歌翻译 API(需要翻墙,无需秘钥,免费)

    谷歌翻译随时可能会改变接口，不保证长期可用。目前测试正常。
    使用的时候注意请求频率，不要频繁请求，否则可能会被谷歌限制。
    """

    api_url = "http://translate.google.com/m?q=%s&tl=%s&sl=%s"

    def __init__(self):
        self.content_validator_handler = ContentValidatorHandler()

    def translate(
        self,
        text: str,
        source: Languages | str = Languages.English,
        target: Languages | str = Languages.Chinese,
    ):
        text: str = text.strip()

        is_content_valid: bool = self.content_validator_handler.validate(text)
        if not is_content_valid:
            raise exceptions.InvalidContentError(f"Invalid content: {text}")

        source: str = self._trans_language(source)
        target: str = self._trans_language(target)

        # 该方法来自 https://blog.csdn.net/wtl1992/article/details/135117192
        text = parse.quote(text)
        url = self.api_url % (text, target, source)

        # 使用 urllib 发起请求
        try:
            response = request.urlopen(url)
            data = response.read().decode("utf-8")
        except urllib.error.HTTPError as e:
            raise exceptions.RequestError(str(e))
        except urllib.error.URLError as e:
            raise exceptions.RequestError(str(e))
        except Exception as e:
            raise exceptions.UnknownError(str(e))

        expr = r'(?s)class="(?:t0|result-container)">(.*?)<'
        result = re.findall(expr, data)
        if len(result) == 0:
            return ""

        return html.unescape(result[0])

    def _trans_language(self, language: Languages | str) -> str:
        """转换语言代码为支持的格式"""
        if isinstance(language, Languages):
            language = language.value

        trans_dict = {
            "auto": "auto",
            "zh": "zh-CN",
            "en": "en",
            "ja": "ja",
            "kor": "ko",
            "ru": "ru",
        }
        return trans_dict.get(language) or language
