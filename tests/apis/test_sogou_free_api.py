import pytest
from translation_hub.apis.sogou_free_api import SoGouFreeApi
from translation_hub.core.enums import Languages
from translation_hub import exceptions


class TestSoGouFreeApi:
    @pytest.mark.parametrize(
        "text,source,target,result",
        [
            # 中英互译
            ("Hello", Languages.English, Languages.Chinese, "你好"),
            ("Hello world", Languages.English, Languages.Chinese, "你好世界"),
            ("你好，世界", Languages.Chinese, Languages.English, "hello,world!"),
            # 中文与其他语言互译
            ("你好", Languages.Chinese, Languages.Japanese, "こんにちは"),
            ("你好", Languages.Chinese, Languages.Russia, "Привет."),
            ("你好", Languages.Chinese, Languages.Korea, "안녕하세요"),
            # 其他语言互译
            ("Hello", Languages.English, Languages.Japanese, "こんにちは"),
            ("こんにちは", Languages.Japanese, Languages.Russia, "Привет."),
            ("Привет", Languages.Russia, Languages.Korea, "안녕하세요"),
            # 字符串语言代码
            ("Hello", "en", "zh", "你好"),
            ("你好", "zh", "en", "hello"),
        ],
    )
    def test_sogou_free_api(
        self, text: str, source: Languages, target: Languages, result: str
    ):
        """测试正常翻译功能"""
        sogou_api = SoGouFreeApi()
        response = sogou_api.translate(text, source, target)
        assert response == result

    def test_empty_text(self):
        """测试空文本"""
        sogou_api = SoGouFreeApi()
        with pytest.raises(exceptions.InvalidContentError):
            sogou_api.translate("", Languages.Chinese, Languages.English)
