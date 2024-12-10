import json

import pytest
import os
from unittest.mock import patch
from translation_hub.apis.aliyun_api import AliyunApi
from translation_hub.core.enums import Languages
from translation_hub import exceptions
from translation_hub.config import cfg


class TestAliyunApi:
    @pytest.fixture
    def api_credentials(self):
        return {
            "api_id": cfg.get(cfg.AliyunAppId),
            "api_key": cfg.get(cfg.AliyunSecretKey),
        }

    @pytest.fixture
    def aliyun_api(self, api_credentials):
        return AliyunApi(
            api_id=api_credentials["api_id"], api_key=api_credentials["api_key"]
        )

    @pytest.fixture
    def mock_successful_response(self):
        return {
            "RequestId": "test-request-id",
            "Data": {"WordCount": "2", "Translated": "你好"},
            "Code": "200",
        }

    def test_init_with_valid_credentials(self, api_credentials):
        """测试使用有效凭据初始化API"""
        api = AliyunApi(
            api_id=api_credentials["api_id"], api_key=api_credentials["api_key"]
        )
        assert api.api_id == api_credentials["api_id"]
        assert api.api_key == api_credentials["api_key"]

    def test_init_with_environment_variables(self):
        """测试从环境变量获取凭据"""
        with patch.dict(
            os.environ,
            {"AliyunAppId": "env_idaaaaaaaaaa", "AliyunSecretKey": "env_keyaaaaaaaaaa"},
        ):
            api = AliyunApi()
            assert api.api_id == "env_idaaaaaaaaaa"
            assert api.api_key == "env_keyaaaaaaaaaa"

    def test_translate_successful(self, aliyun_api, mock_successful_response):
        """测试正常翻译流程"""
        result = aliyun_api.translate("Hello", Languages.English, Languages.Chinese)
        assert result == "你好"

    def test_translate_server_error(self, aliyun_api):
        """测试服务器错误情况"""
        error_response = {
            "Code": "10033",
            "Message": "语种拼写错误",
            "RequestId": "test-error-id",
        }
        with patch("translation_hub.apis.aliyun_api.request") as mock_request:
            mock_request.return_value = json.dumps(error_response)
            with pytest.raises(exceptions.ServerError):
                aliyun_api.translate("Hello", "random", Languages.Chinese)

    def test_trans_language_with_enum(self, aliyun_api):
        """测试语言代码转换 - 枚举输入"""
        assert aliyun_api._trans_language(Languages.Chinese) == "zh"
        assert aliyun_api._trans_language(Languages.English) == "en"
        assert aliyun_api._trans_language(Languages.Japanese) == "ja"
