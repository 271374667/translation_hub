from translation_hub.apis.google_free_api import GoogleFreeApi
from translation_hub.core.enums import Languages
import pytest


class TestGoogleApi:
    @pytest.mark.parametrize('text, source, target, result', [
        # 中英互译
        ("你好", Languages.Chinese, Languages.English, "Hello"),
        ("Hello", Languages.English, Languages.Chinese, "你好"),
        # 中日互译
        ("你好", Languages.Chinese, Languages.Japanese, "こんにちは"),
        ("こんにちは", Languages.Japanese, Languages.Chinese, "你好"),
        # 其他测试
        ("你吃饭了么?", Languages.Chinese, Languages.Japanese, "食事はありましたか？"),
        ("about your situation", Languages.English, Languages.Chinese, "关于您的情况"),
        ("about your situation", Languages.English, Languages.Korea, "당신의 상황에 대해"),
        ("about your situation", Languages.English, Languages.Russia, "о вашей ситуации"),
        ("about your situation", Languages.Auto, Languages.Chinese, "关于您的情况"),
    ])
    def test_translate_successful(self, text: str, source: Languages|str, target: Languages|str, result: str):
        """测试正常翻译流程"""
        google_api = GoogleFreeApi()
        response = google_api.translate(text, source, target)
        assert response == result
