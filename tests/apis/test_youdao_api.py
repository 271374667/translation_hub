import json
import os
import pytest
from translation_hub.apis.youdao_api import YoudaoApi
from translation_hub.core.enums import Languages
from unittest.mock import patch
from translation_hub import exceptions
from translation_hub.config import cfg


@pytest.fixture
def youdao_api():
    return YoudaoApi(
        api_id=cfg.get(cfg.YoudaoAppId), api_key=cfg.get(cfg.YoudaoSecretKey)
    )


class TestYoudaoApi:
    @patch.dict(
        os.environ, {"YoudaoAppId": "env_api_id", "YoudaoSecretKey": "env_api_key"}
    )
    def test_get_api_id_and_key_from_env(self):
        api = YoudaoApi()
        assert api.api_id == "env_api_id"
        assert api.api_key == "env_api_key"

    @patch.object(
        cfg,
        "get",
        side_effect=lambda key: "cfg_api_id"
        if key == cfg.YoudaoAppId
        else "cfg_api_key",
    )
    def test_get_api_id_and_key_from_cfg(self, mock_cfg):
        api = YoudaoApi()
        assert api.api_id == "cfg_api_id"
        assert api.api_key == "cfg_api_key"

    def test_get_api_id_and_key_directly(self):
        api = YoudaoApi(api_id="direct_api_id", api_key="direct_api_key")
        assert api.api_id == "direct_api_id"
        assert api.api_key == "direct_api_key"

    @patch.dict(os.environ, {}, clear=True)
    @patch.object(cfg, "get", return_value=None)
    def test_get_api_id_and_key_error(self, mock_cfg):
        with pytest.raises(exceptions.InvalidSecretKeyError):
            YoudaoApi()

    def test_translates_text_correctly(self, youdao_api):
        result = youdao_api.translate("你好,世界", Languages.Chinese, Languages.English)
        assert result == "Hello, world"

    def test_handles_key_error(self, youdao_api):
        with patch("translation_hub.apis.youdao_api.request") as mock_request:
            mock_request.return_value = "{}"
            with pytest.raises(exceptions.JsonDecodeError):
                youdao_api.translate("你好,世界", Languages.Chinese, Languages.English)

    def test_handles_json_decode_error(self, youdao_api):
        with patch("translation_hub.apis.youdao_api.request") as mock_request:
            mock_request.return_value = "Invalid JSON"
            with pytest.raises(exceptions.JsonDecodeError):
                youdao_api.translate("你好,世界", Languages.Chinese, Languages.English)

    def test_handles_generic_exception(self, youdao_api):
        with patch("translation_hub.apis.youdao_api.request") as mock_request:
            mock_request.side_effect = Exception("Some error")
            with pytest.raises(exceptions.UnknownError):
                youdao_api.translate("你好,世界", Languages.Chinese, Languages.English)

    def test_handles_request_error_101(self, youdao_api):
        with patch("translation_hub.apis.youdao_api.request") as mock_request:
            mock_request.return_value = json.dumps({"errorCode": "101"})
            with pytest.raises(exceptions.RequestError):
                youdao_api.translate("你好,世界", Languages.Chinese, Languages.English)

    def test_handles_request_error_102(self, youdao_api):
        with patch("translation_hub.apis.youdao_api.request") as mock_request:
            mock_request.return_value = json.dumps({"errorCode": "102"})
            with pytest.raises(exceptions.RequestError):
                youdao_api.translate("你好,世界", Languages.Chinese, Languages.English)

    def test_handles_request_error_103(self, youdao_api):
        with patch("translation_hub.apis.youdao_api.request") as mock_request:
            mock_request.return_value = json.dumps({"errorCode": "103"})
            with pytest.raises(exceptions.RequestError):
                youdao_api.translate("你好,世界", Languages.Chinese, Languages.English)

    def test_handles_unknown_error(self, youdao_api):
        with patch("translation_hub.apis.youdao_api.request") as mock_request:
            mock_request.return_value = json.dumps({"errorCode": "99999"})
            with pytest.raises(exceptions.RequestError):
                youdao_api.translate("你好,世界", Languages.Chinese, Languages.English)
