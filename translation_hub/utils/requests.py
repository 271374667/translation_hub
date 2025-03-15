import urllib.request
import urllib.parse
import json
from typing import Optional, Dict


def request(
    url: str,
    headers: Dict[str, str],
    payload: Optional[Dict[str, str]] = None,
    data: Optional[Dict[str, str]] = None,
    json_data: Optional[Dict] = None,
) -> str:
    """
    发送 HTTP 请求并返回响应内容。

    参数:
        url (str): 请求的 URL。
        headers (dict): 请求头。
        payload (dict, optional): 查询参数，将附加到 URL 中。
        data (dict, optional): 表单数据（application/x-www-form-urlencoded）。
        json_data (dict, optional): JSON 数据（application/json）。

    返回:
        str: 响应的内容。

    示例:
        response = request(
            url="https://api.example.com/data",
            headers={"Authorization": "Bearer token"},
            payload={"query": "value"},
            data={"key": "value"},
            json_data={"json_key": "json_value"}
        )
    """
    # 处理查询参数（payload）
    if payload:
        query_string = urllib.parse.urlencode(payload)
        separator = "&" if "?" in url else "?"
        url = f"{url}{separator}{query_string}"

    # 初始化请求数据和Content-Type
    request_data = None
    if json_data is not None:
        request_data = json.dumps(json_data).encode("utf-8")
        headers["Content-Type"] = "application/json"
    elif data is not None:
        request_data = urllib.parse.urlencode(data).encode("utf-8")
        headers["Content-Type"] = "application/x-www-form-urlencoded"

    # 创建请求对象
    req = urllib.request.Request(url, headers=headers, data=request_data)

    with urllib.request.urlopen(req) as response:
        charset = response.headers.get_content_charset() or "utf-8"
        return response.read().decode(charset)
