import hashlib
import time
import urllib.request
import urllib.parse
import json
import uuid
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


# if __name__ == "__main__":
#     # 示例 1: GET 请求，带查询参数
#     response = request(
#         url="https://httpbin.org/get",
#         headers={"User-Agent": "Mozilla/5.0"},
#         payload={"search": "python", "page": "1"},
#     )
#     print("GET Response:", response)
#
#     # 示例 2: POST 请求，发送表单数据
#     response = request(
#         url="https://httpbin.org/post",
#         headers={"User-Agent": "Mozilla/5.0"},
#         data={"username": "test", "password": "1234"},
#     )
#     print("POST Form Response:", response)
#
#     # 示例 3: POST 请求，发送 JSON 数据
#     response = request(
#         url="https://httpbin.org/post",
#         headers={"User-Agent": "Mozilla/5.0"},
#         json_data={"key": "value", "number": 42},
#     )
#     print("POST JSON Response:", response)

if __name__ == "__main__":
    YOUDAO_URL = "https://openapi.youdao.com/api"
    APP_KEY = "2e276409e88add8a"
    APP_SECRET = "JXROFWyhCl8REgF9f8M6k4LAc2FK4HUv"

    def encrypt(sign_str):
        hash_algorithm = hashlib.sha256()
        hash_algorithm.update(sign_str.encode("utf-8"))
        return hash_algorithm.hexdigest()

    def truncate(q):
        if q is None:
            return None
        size = len(q)
        return q if size <= 20 else q[0:10] + str(size) + q[size - 10 : size]

    def do_request(data):
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        return request(YOUDAO_URL, data=data, headers=headers)

    q = "你好,世界"

    data = {}
    data["from"] = "源语言"
    data["to"] = "目标语言"
    data["signType"] = "v3"
    curtime = str(int(time.time()))
    data["curtime"] = curtime
    salt = str(uuid.uuid1())
    signStr = APP_KEY + truncate(q) + salt + curtime + APP_SECRET
    sign = encrypt(signStr)
    data["appKey"] = APP_KEY
    data["q"] = q
    data["salt"] = salt
    data["sign"] = sign

    response = do_request(data)
    print(response)
