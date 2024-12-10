import json
import os
import pytest
from translation_hub.apis.baidu_api import BaiduAPI
from translation_hub.core.enums import Languages
from unittest.mock import patch
from translation_hub import exceptions
from translation_hub.config import cfg


@pytest.fixture
def baidu_api():
    return BaiduAPI(api_id=cfg.get(cfg.BaiduAppId), api_key=cfg.get(cfg.BaiduSecretKey))


class TestBaiduAPI:
    @patch.dict(
        os.environ, {"BaiduAppId": "env_api_id", "BaiduSecretKey": "env_api_key"}
    )
    def test_get_api_id_and_key_from_env(self):
        api = BaiduAPI()
        assert api.api_id == "env_api_id"
        assert api.api_key == "env_api_key"

    @patch.object(
        cfg,
        "get",
        side_effect=lambda key: "cfg_api_id"
        if key == cfg.BaiduAppId
        else "cfg_api_key",
    )
    def test_get_api_id_and_key_from_cfg(self, mock_cfg):
        api = BaiduAPI()
        assert api.api_id == "cfg_api_id"
        assert api.api_key == "cfg_api_key"

    def test_get_api_id_and_key_directly(self):
        api = BaiduAPI(api_id="direct_api_id", api_key="direct_api_key")
        assert api.api_id == "direct_api_id"
        assert api.api_key == "direct_api_key"

    @patch.dict(os.environ, {}, clear=True)
    @patch.object(cfg, "get", return_value=None)
    def test_get_api_id_and_key_error(self, mock_cfg):
        with pytest.raises(exceptions.InvalidSecretKeyError):
            BaiduAPI()

    def test_translates_text_correctly(self, baidu_api):
        with patch("translation_hub.apis.baidu_api.request") as mock_request:
            mock_request.return_value = json.dumps(
                {
                    "from": "en",
                    "to": "zh",
                    "trans_result": [{"src": "Hello", "dst": "你好"}],
                }
            )
            result = baidu_api.translate("Hello", Languages.English, Languages.Chinese)
            assert result == "你好"

    def test_translates_text_with_network(self, baidu_api):
        result = baidu_api.translate(
            "这是一个测试", Languages.Chinese, Languages.English
        )
        assert result == "This is a test"

    def test_translates_blank_text(self, baidu_api):
        with pytest.raises(exceptions.InvalidContentError):
            baidu_api.translate("", Languages.English, Languages.Chinese)

    def test_handles_key_error(self, baidu_api):
        with patch("translation_hub.apis.baidu_api.request") as mock_request:
            mock_request.return_value = "{}"
            with pytest.raises(exceptions.ResponseError):
                baidu_api.translate("Hello", Languages.English, Languages.Chinese)

    def test_handles_json_decode_error(self, baidu_api):
        with patch("translation_hub.apis.baidu_api.request") as mock_request:
            mock_request.return_value = "Invalid JSON"
            with pytest.raises(exceptions.JsonDecodeError):
                baidu_api.translate("Hello", Languages.English, Languages.Chinese)

    def test_handles_generic_exception(self, baidu_api):
        with patch("translation_hub.apis.baidu_api.request") as mock_request:
            mock_request.side_effect = Exception("Some error")
            with pytest.raises(exceptions.RequestError):
                baidu_api.translate("Hello", Languages.English, Languages.Chinese)

    def test_translates_with_string_language(self, baidu_api):
        with patch("translation_hub.apis.baidu_api.request") as mock_request:
            mock_request.return_value = json.dumps({"trans_result": [{"dst": "你好"}]})
            result = baidu_api.translate("Hello", "en", "zh")
            assert result == "你好"

    def test_handles_request_timeout_error(self, baidu_api):
        with patch("translation_hub.apis.baidu_api.request") as mock_request:
            mock_request.return_value = json.dumps(
                {"error_code": "52001", "error_msg": "请求超时"}
            )
            with pytest.raises(exceptions.ServerError):
                baidu_api.translate("Hello", Languages.English, Languages.Chinese)

    def test_handles_system_error(self, baidu_api):
        with patch("translation_hub.apis.baidu_api.request") as mock_request:
            mock_request.return_value = json.dumps(
                {"error_code": "52002", "error_msg": "系统错误"}
            )
            with pytest.raises(exceptions.ServerError):
                baidu_api.translate("Hello", Languages.English, Languages.Chinese)

    def test_handles_unauthorized_user_error(self, baidu_api):
        with patch("translation_hub.apis.baidu_api.request") as mock_request:
            mock_request.return_value = json.dumps(
                {"error_code": "52003", "error_msg": "未授权用户"}
            )
            with pytest.raises(exceptions.ServerError):
                baidu_api.translate("Hello", Languages.English, Languages.Chinese)

    def test_handles_missing_parameter_error(self, baidu_api):
        with patch("translation_hub.apis.baidu_api.request") as mock_request:
            mock_request.return_value = json.dumps(
                {"error_code": "54000", "error_msg": "必填参数为空"}
            )
            with pytest.raises(exceptions.ServerError):
                baidu_api.translate("Hello", Languages.English, Languages.Chinese)

    def test_handles_signature_error(self, baidu_api):
        with patch("translation_hub.apis.baidu_api.request") as mock_request:
            mock_request.return_value = json.dumps(
                {"error_code": "54001", "error_msg": "签名错误"}
            )
            with pytest.raises(exceptions.ServerError):
                baidu_api.translate("Hello", Languages.English, Languages.Chinese)

    def test_handles_rate_limit_error(self, baidu_api):
        with patch("translation_hub.apis.baidu_api.request") as mock_request:
            mock_request.return_value = json.dumps(
                {"error_code": "54003", "error_msg": "访问频率受限"}
            )
            with pytest.raises(exceptions.ServerError):
                baidu_api.translate("Hello", Languages.English, Languages.Chinese)

    def test_handles_insufficient_balance_error(self, baidu_api):
        with patch("translation_hub.apis.baidu_api.request") as mock_request:
            mock_request.return_value = json.dumps(
                {"error_code": "54004", "error_msg": "账户余额不足"}
            )
            with pytest.raises(exceptions.ServerError):
                baidu_api.translate("Hello", Languages.English, Languages.Chinese)

    def test_handles_frequent_long_query_error(self, baidu_api):
        with patch("translation_hub.apis.baidu_api.request") as mock_request:
            mock_request.return_value = json.dumps(
                {"error_code": "54005", "error_msg": "长query请求频繁"}
            )
            with pytest.raises(exceptions.ServerError):
                baidu_api.translate("Hello", Languages.English, Languages.Chinese)

    def test_handles_invalid_client_ip_error(self, baidu_api):
        with patch("translation_hub.apis.baidu_api.request") as mock_request:
            mock_request.return_value = json.dumps(
                {"error_code": "58000", "error_msg": "客户端IP非法"}
            )
            with pytest.raises(exceptions.ServerError):
                baidu_api.translate("Hello", Languages.English, Languages.Chinese)

    def test_handles_unsupported_language_direction_error(self, baidu_api):
        with patch("translation_hub.apis.baidu_api.request") as mock_request:
            mock_request.return_value = json.dumps(
                {"error_code": "58001", "error_msg": "译文语言方向不支持"}
            )
            with pytest.raises(exceptions.ServerError):
                baidu_api.translate("Hello", Languages.English, Languages.Chinese)

    def test_handles_service_closed_error(self, baidu_api):
        with patch("translation_hub.apis.baidu_api.request") as mock_request:
            mock_request.return_value = json.dumps(
                {"error_code": "58002", "error_msg": "服务当前已关闭"}
            )
            with pytest.raises(exceptions.ServerError):
                baidu_api.translate("Hello", Languages.English, Languages.Chinese)

    def test_handles_ip_banned_error(self, baidu_api):
        with patch("translation_hub.apis.baidu_api.request") as mock_request:
            mock_request.return_value = json.dumps(
                {"error_code": "58003", "error_msg": "此IP已被封禁"}
            )
            with pytest.raises(exceptions.ServerError):
                baidu_api.translate("Hello", Languages.English, Languages.Chinese)

    def test_handles_authentication_failed_error(self, baidu_api):
        with patch("translation_hub.apis.baidu_api.request") as mock_request:
            mock_request.return_value = json.dumps(
                {"error_code": "90107", "error_msg": "认证未通过或未生效"}
            )
            with pytest.raises(exceptions.ServerError):
                baidu_api.translate("Hello", Languages.English, Languages.Chinese)

    def test_handles_security_risk_error(self, baidu_api):
        with patch("translation_hub.apis.baidu_api.request") as mock_request:
            mock_request.return_value = json.dumps(
                {"error_code": "20003", "error_msg": "请求内容存在安全风险"}
            )
            with pytest.raises(exceptions.ServerError):
                baidu_api.translate("Hello", Languages.English, Languages.Chinese)

    def test_handles_unknown_error(self, baidu_api):
        with patch("translation_hub.apis.baidu_api.request") as mock_request:
            mock_request.return_value = json.dumps(
                {"error_code": "99999", "error_msg": "未知错误"}
            )
            with pytest.raises(exceptions.UnknownError):
                baidu_api.translate("Hello", Languages.English, Languages.Chinese)
