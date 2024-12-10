from translation_hub.validators.validator import Validator


class EmptyStringValidator(Validator):
    """空字符串验证器"""

    def validate(self, value: str) -> bool:
        return bool(value.strip())


class WrongLengthValidator(Validator):
    """长度验证器"""

    def validate(self, value: str, min_length: int = 10, max_length: int = 100) -> bool:
        return min_length <= len(value) <= max_length


class NumberOnlyValidator(Validator):
    """纯数字验证器"""

    def validate(self, value: str) -> bool:
        return value.isdigit()


class LetterOnlyValidator(Validator):
    """纯字母验证器"""

    def validate(self, value: str) -> bool:
        return value.isalpha()


class HasNumberAndLetterValidator(Validator):
    """同时包含数字和字母验证器"""

    def validate(self, value: str) -> bool:
        return any(c.isdigit() for c in value) and any(c.isalpha() for c in value)


class HasSpecialCharValidator(Validator):
    """特殊字符验证器"""

    def validate(self, value: str) -> bool:
        return not value.isalnum()
