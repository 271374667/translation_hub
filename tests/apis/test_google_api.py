from translation_hub.apis.google_api import GoogleApi
from translation_hub.core.enums import Languages
import pytest


class TestGoogleApi:
    @pytest.fixture
    def google_api(self):
        return GoogleApi()

    def test_translate_successful(self, google_api: GoogleApi):
        """测试正常翻译流程"""
        # 中文翻译为日文
        result = google_api.translate(
            "你吃饭了么?", Languages.Chinese, Languages.Japanese
        )
        assert result == "食べましたか？"

        # 英文翻译为中文
        result = google_api.translate(
            "about your situation", Languages.English, Languages.Chinese
        )
        assert result == "关于你的情况"

        # 英语翻译成韩文
        result = google_api.translate(
            "about your situation", Languages.English, Languages.Korea
        )
        assert result == "당신의 상황에 대해서"

        # 英文翻译成俄文
        result = google_api.translate(
            "about your situation", Languages.English, Languages.Russia
        )
        assert result == "о вашей ситуации"

        # 自动翻译成中文
        result = google_api.translate(
            "about your situation", Languages.Auto, Languages.Chinese
        )
        assert result == "关于你的情况"
