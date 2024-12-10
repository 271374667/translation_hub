class RequestError(Exception):
    def __init__(self, message="请求错误: 请重试"):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f"RequestError: {self.message}"


class ResponseError(Exception):
    def __init__(self, message="响应错误: 请重试"):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f"ResponseError: {self.message}"


class ServerError(Exception):
    def __init__(self, message="服务器错误: 请重试"):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f"ServerError: {self.message}"


class InvalidSecretKeyError(Exception):
    def __init__(self, message="密钥错误: 请检查密钥是否正确"):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f"InvalidSecretKeyError: {self.message}"


class InvalidContentError(Exception):
    def __init__(self, message="请求内容错误: 请检查请求内容"):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f"InvalidContentError: {self.message}"


class JsonDecodeError(Exception):
    def __init__(self, message="无法解码 JSON: 不合法的 JSON"):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f"JsonDecodeError: {self.message}"


class UnknownError(Exception):
    def __init__(self, message="未知错误: 请重试或者前往github提交issue"):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f"UnknownError: {self.message}"
