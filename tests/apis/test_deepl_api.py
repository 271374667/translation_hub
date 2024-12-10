import json
import os
import urllib
import urllib.error

import pytest
from translation_hub.apis.deepl_api import DeeplApi
from translation_hub.core.enums import Languages
from unittest.mock import patch
from translation_hub import exceptions
from translation_hub.config import cfg


@pytest.fixture
def deepl_api():
    return DeeplApi(api_key=cfg.get(cfg.DeeplApiKey))


class TestDeeplApi:
    @patch.dict(os.environ, {"DeeplApiKey": "env_api_key"})
    def test_get_api_key_from_env(self):
        api = DeeplApi()
        assert api.api_key == "env_api_key"

    @patch.object(
        cfg,
        "get",
        side_effect=lambda key: "cfg_api_key" if key == cfg.DeeplApiKey else None,
    )
    def test_get_api_key_from_cfg(self, mock_cfg):
        api = DeeplApi()
        assert api.api_key == "cfg_api_key"

    def test_get_api_key_directly(self):
        api = DeeplApi(api_key="direct_api_key")
        assert api.api_key == "direct_api_key"

    @patch.dict(os.environ, {}, clear=True)
    @patch.object(cfg, "get", return_value=None)
    def test_get_api_key_error(self, mock_cfg):
        with pytest.raises(exceptions.InvalidSecretKeyError):
            DeeplApi()

    def test_translates_text_correctly(self, deepl_api):
        with patch("translation_hub.apis.deepl_api.request") as mock_request:
            mock_request.return_value = json.dumps(
                {"translations": [{"text": "你好，世界"}]}
            )
            result = deepl_api.translate(
                "Hello, world!", Languages.English, Languages.Chinese
            )
            assert result == "你好，世界"

    def test_translates_text_correctly_with_network(self, deepl_api):
        result = deepl_api.translate(
            "Hello, world!", Languages.English, Languages.Chinese
        )
        assert result == "你好，世界"

    def test_translates_text_correctly_with_auto_language(self, deepl_api):
        with patch("translation_hub.apis.deepl_api.request") as mock_request:
            mock_request.return_value = json.dumps(
                {
                    "translations": [
                        {"detected_source_language": "ZH", "text": "Hello, world."}
                    ]
                }
            )
            result = deepl_api.translate(
                "Hello, world!", Languages.Auto, Languages.English
            )
            assert result == "Hello, world."

    def test_handles_key_error(self, deepl_api):
        with patch("translation_hub.apis.deepl_api.request") as mock_request:
            mock_request.return_value = "{}"
            with pytest.raises(exceptions.ResponseError):
                deepl_api.translate(
                    "Hello, world!", Languages.English, Languages.Chinese
                )

    def test_handles_json_decode_error(self, deepl_api):
        with patch("translation_hub.apis.deepl_api.request") as mock_request:
            mock_request.return_value = "Invalid JSON"
            with pytest.raises(exceptions.JsonDecodeError):
                deepl_api.translate(
                    "Hello, world!", Languages.English, Languages.Chinese
                )

    def test_handles_generic_exception(self, deepl_api):
        with patch("translation_hub.apis.deepl_api.request") as mock_request:
            mock_request.side_effect = Exception("Some error")
            with pytest.raises(exceptions.UnknownError):
                deepl_api.translate(
                    "Hello, world!", Languages.English, Languages.Chinese
                )

    def test_translates_with_string_language(self, deepl_api):
        with patch("translation_hub.apis.deepl_api.request") as mock_request:
            mock_request.return_value = json.dumps(
                {"translations": [{"text": "你好，世界"}]}
            )
            result = deepl_api.translate("Hello, world!", "en", "zh")
            assert result == "你好，世界"

    def test_handles_request_error_403(self, deepl_api):
        with patch("translation_hub.apis.deepl_api.request") as mock_request:
            mock_request.side_effect = urllib.error.HTTPError(
                url="", code=403, msg="", hdrs={}, fp=None
            )
            with pytest.raises(exceptions.RequestError):
                deepl_api.translate(
                    "Hello, world!", Languages.English, Languages.Chinese
                )

    def test_handles_request_error_429(self, deepl_api):
        with patch("translation_hub.apis.deepl_api.request") as mock_request:
            mock_request.side_effect = urllib.error.HTTPError(
                url="", code=429, msg="", hdrs={}, fp=None
            )
            with pytest.raises(exceptions.RequestError):
                deepl_api.translate(
                    "Hello, world!", Languages.English, Languages.Chinese
                )

    def test_handles_request_error_456(self, deepl_api):
        with patch("translation_hub.apis.deepl_api.request") as mock_request:
            mock_request.side_effect = urllib.error.HTTPError(
                url="", code=456, msg="", hdrs={}, fp=None
            )
            with pytest.raises(exceptions.RequestError):
                deepl_api.translate(
                    "Hello, world!", Languages.English, Languages.Chinese
                )

    def test_handles_request_error_500(self, deepl_api):
        with patch("translation_hub.apis.deepl_api.request") as mock_request:
            mock_request.side_effect = urllib.error.HTTPError(
                url="", code=500, msg="", hdrs={}, fp=None
            )
            with pytest.raises(exceptions.ServerError):
                deepl_api.translate(
                    "Hello, world!", Languages.English, Languages.Chinese
                )

    def test_handles_unknown_error(self, deepl_api):
        with patch("translation_hub.apis.deepl_api.request") as mock_request:
            mock_request.side_effect = urllib.error.HTTPError(
                url="", code=999, msg="", hdrs={}, fp=None
            )
            with pytest.raises(exceptions.UnknownError):
                deepl_api.translate(
                    "Hello, world!", Languages.English, Languages.Chinese
                )
