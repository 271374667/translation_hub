import pytest
from translation_hub.apis.bing_free_api import BingFreeApi
from translation_hub.core.enums import Languages
from translation_hub import exceptions


@pytest.fixture
def bing_free_api():
    return BingFreeApi()


class TestBingFreeApi:
    @pytest.mark.parametrize(
        "text,source,target,expected",
        [
            # 中英互译
            ("Hello", Languages.English, Languages.Chinese, "你好"),
            ("Hello world", Languages.English, Languages.Chinese, "世界"),
            ("你好，世界", Languages.Chinese, Languages.English, "Hello, world"),
            # 中文与其他语言互译
            ("你好", Languages.Chinese, Languages.Japanese, "こんにちは"),
            ("你好", Languages.Chinese, Languages.Russia, "Привет"),
            ("你好", Languages.Chinese, Languages.Korea, "안녕하세요"),
            # 其他语言互译
            ("Hello", Languages.English, Languages.Japanese, "こんにちは"),
            ("こんにちは", Languages.Japanese, Languages.Russia, "Привет"),
            ("Привет", Languages.Russia, Languages.Korea, "안녕하세요"),
            # 字符串语言代码
            ("Hello", "en", "zh", "你好"),
            ("你好", "zh", "en", "Hello"),
        ],
    )
    def test_translate_languages(self, bing_free_api, text, source, target, expected):
        # 直接调用翻译 API 而不使用 mock
        result = bing_free_api.translate(text, source, target)
        # 断言翻译结果与期望的结果匹配
        # 由于翻译可能有多种可能的正确表达，我们检查结果是否包含关键部分
        assert result.lower() in expected.lower() or expected.lower() in result.lower()

    def test_auto_detection(self, bing_free_api):
        # 测试自动检测语言功能
        result = bing_free_api.translate("你好", Languages.Auto, Languages.English)
        assert "hello" in result.lower()

        result = bing_free_api.translate("Hello", Languages.Auto, Languages.Chinese)
        assert "你好" in result

    @pytest.mark.parametrize(
        "source_lang,target_lang",
        [
            (Languages.Chinese, Languages.English),
            (Languages.English, Languages.Chinese),
            (Languages.Japanese, Languages.Chinese),
            (Languages.Russia, Languages.Chinese),
            (Languages.Korea, Languages.English),
        ],
    )
    def test_translate_empty_text(self, bing_free_api, source_lang, target_lang):
        # 测试空文本
        with pytest.raises(exceptions.InvalidContentError):
            bing_free_api.translate("", source_lang, target_lang)

    def test_auto_detection_invalid(self, bing_free_api):
        # 测试自动检测语言功能
        with pytest.raises(exceptions.ResponseError):
            bing_free_api.translate("你好", Languages.Auto, "invalid_language")

        # 测试中英自动互译
        result = bing_free_api.translate("你好", Languages.Auto, Languages.English)
        assert "hello" in result.lower()
        result = bing_free_api.translate("Hello", Languages.Auto, Languages.Chinese)
        assert "你好" in result.lower()
