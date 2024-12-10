import json
import os
import time
import urllib
import urllib.error

import pytest
from translation_hub.apis.tencent_api import TencentApi
from translation_hub.core.enums import Languages
from unittest.mock import patch, MagicMock
from translation_hub import exceptions
from translation_hub.config import cfg


@pytest.fixture
def tencent_api():
    return TencentApi(
        api_id=cfg.get(cfg.TencentAppId),
        api_key=cfg.get(cfg.TencentSecretKey),
    )


class TestTencentApi:
    @patch.dict(
        os.environ, {"TencentAppId": "env_api_id", "TencentSecretKey": "env_api_key"}
    )
    def test_get_api_id_and_key_from_env(self):
        api = TencentApi()
        assert api.api_id == "env_api_id"
        assert api.api_key == "env_api_key"

    @patch.object(
        cfg,
        "get",
        side_effect=lambda key: "cfg_api_id"
        if key == cfg.TencentAppId
        else "cfg_api_key",
    )
    def test_get_api_id_and_key_from_cfg(self, mock_cfg):
        api = TencentApi()
        assert api.api_id == "cfg_api_id"
        assert api.api_key == "cfg_api_key"

    def test_get_api_id_and_key_directly(self):
        api = TencentApi(api_id="direct_api_id", api_key="direct_api_key")
        assert api.api_id == "direct_api_id"
        assert api.api_key == "direct_api_key"

    @patch.dict(os.environ, {}, clear=True)
    @patch.object(cfg, "get", return_value=None)
    def test_get_api_id_and_key_error(self, mock_cfg):
        with pytest.raises(exceptions.InvalidSecretKeyError):
            TencentApi()

    def test_translates_text_correctly(self, tencent_api):
        result = tencent_api.translate(
            "Hello, world!", Languages.English, Languages.Chinese
        )
        assert result == "你好，世界！"

    def test_handles_invalid_content_error(self, tencent_api):
        with pytest.raises(exceptions.InvalidContentError):
            tencent_api.translate("", Languages.English, Languages.Chinese)

    def test_request_error(self, tencent_api):
        with patch(
            "translation_hub.apis.tencent_api.urllib.request.urlopen"
        ) as mock_urlopen:
            # 创建一个模拟的响应对象
            # 配置mock_urlopen的返回值，以支持with语句
            with pytest.raises(exceptions.RequestError):
                mock_urlopen.side_effect = urllib.error.HTTPError(
                    url="", code=403, msg="", hdrs=None, fp=None
                )
                tencent_api.translate(
                    "Hello, world!", Languages.English, Languages.Chinese
                )

    def test_handles_server_error(self, tencent_api):
        with patch(
            "translation_hub.apis.tencent_api.urllib.request.urlopen"
        ) as mock_urlopen:
            # 创建一个模拟的上下文管理器对象
            mock_cm = MagicMock()
            mock_response = mock_cm.__enter__.return_value
            mock_response.read.return_value = json.dumps(
                {
                    "Response": {
                        "Error": {
                            "Code": "FailedOperation",
                            "Message": "Server error occurred",
                        },
                        "RequestId": "test-request-id",
                    }
                }
            ).encode("utf-8")
            mock_urlopen.return_value = mock_cm

            with pytest.raises(exceptions.ServerError):
                tencent_api.translate(
                    "Hello, world!", Languages.English, Languages.Chinese
                )

    def test_handles_http_error(self, tencent_api):
        with patch(
            "urllib.request.urlopen",
            side_effect=urllib.error.HTTPError(
                url="", code=403, msg="", hdrs=None, fp=None
            ),
        ):
            with pytest.raises(exceptions.RequestError):
                tencent_api.translate(
                    "Hello, world!", Languages.English, Languages.Chinese
                )

    def test_handles_json_decode_error(self, tencent_api):
        with patch(
            "translation_hub.apis.tencent_api.urllib.request.urlopen"
        ) as mock_urlopen:
            # 创建一个模拟的上下文管理器对象
            mock_cm = MagicMock()
            mock_response = mock_cm.__enter__.return_value
            mock_response.read.return_value = b"Invalid JSON {"
            mock_urlopen.return_value = mock_cm

            with pytest.raises(exceptions.JsonDecodeError):
                tencent_api.translate(
                    "Hello, world!", Languages.English, Languages.Chinese
                )

    def test_handles_generic_exception(self, tencent_api):
        with patch("urllib.request.urlopen", side_effect=Exception("Some error")):
            with pytest.raises(exceptions.UnknownError):
                tencent_api.translate(
                    "Hello, world!", Languages.English, Languages.Chinese
                )

    def test_trans_language(self, tencent_api):
        assert tencent_api._trans_language(Languages.English) == "en"
        assert tencent_api._trans_language("en") == "en"

    def test_get_authorization(self, tencent_api):
        payload = {
            "SourceText": "Hello, world!",
            "Source": "en",
            "Target": "zh",
            "ProjectId": 0,
        }
        timestamp = int(time.time())
        authorization = tencent_api._get_authorization(payload, timestamp)
        assert "TC3-HMAC-SHA256" in authorization
