import json
import pytest
from unittest.mock import patch, MagicMock

import requests

from translation_hub.apis.baidu_free_api import BaiduFreeAPI
from translation_hub.core.enums import Languages
from translation_hub import exceptions


@pytest.fixture
def baidu_free_api():
    return BaiduFreeAPI()


class TestBaiduFreeAPI:
    def test_translate_success(self, baidu_free_api):
        result = baidu_free_api.translate("你好", Languages.Chinese, Languages.English)

        assert result == "hello"

        result2 = baidu_free_api.translate(
            "你好世界", Languages.Chinese, Languages.English
        )

        assert result2 == "Hello world"

        result3 = baidu_free_api.translate(
            "Hello world", Languages.English, Languages.Chinese
        )
        assert result3 == "你好，世界"

    def test_extract_translated_text_success(self, baidu_free_api):
        response = (
            'data: {"data":{"list":[{"dst":"Hello world"}]},"Translating":true}\n'
        )
        result = baidu_free_api.extraxt_translated_text(response)
        assert result == "Hello world"

    def test_extract_translated_text_error(self, baidu_free_api):
        response = "Invalid response format"
        with pytest.raises(exceptions.ResponseError):
            baidu_free_api.extraxt_translated_text(response)

    def test_extract_translated_text_multiple_lines(self, baidu_free_api):
        response = 'some random line\ndata: {"data":{"list":[{"dst":"Hello world"}]},"Translating":true}\nmore data'
        result = baidu_free_api.extraxt_translated_text(response)
        assert result == "Hello world"

    def test_translates_blank_text(self, baidu_free_api):
        result = baidu_free_api.translate("", Languages.English, Languages.Chinese)
        assert result == ""

    def test_handles_network_error(self, baidu_free_api):
        with patch("requests.post") as mock_post:
            mock_post.side_effect = requests.RequestException("Network error")

            with pytest.raises(exceptions.RequestError):
                baidu_free_api.translate("Hello", Languages.English, Languages.Chinese)

        with patch("requests.post") as mock_post:
            mock_post.side_effect = json.JSONDecodeError(
                msg="Invalid JSON", doc="", pos=0
            )

            with pytest.raises(exceptions.JsonDecodeError):
                baidu_free_api.translate("Hello", Languages.English, Languages.Chinese)

        with patch("requests.post") as mock_post:
            mock_post.side_effect = Exception("Unknown error")
            with pytest.raises(exceptions.UnknownError):
                baidu_free_api.translate("Hello", Languages.English, Languages.Chinese)

    def test_timestamp_generation(self, baidu_free_api):
        with patch("time.time_ns") as mock_time:
            mock_time.return_value = 1698765432109876543
            with patch("requests.post") as mock_post:
                mock_response = MagicMock()
                mock_response.text = (
                    'data: {"data":{"list":[{"dst":"Hello"}]},"Translating":true}'
                )
                mock_post.return_value = mock_response

                baidu_free_api.translate("Hello", Languages.English, Languages.Chinese)

                _, kwargs = mock_post.call_args
                payload = json.loads(kwargs["data"])
                assert payload["milliTimestamp"] == 1698765432109
