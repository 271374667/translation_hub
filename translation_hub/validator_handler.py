from translation_hub.validators.validator import Validator
from translation_hub.validators import secret_key_validator, content_validator
from abc import ABC


class ValidatorHandler(ABC):
    def __init__(self):
        self.validators = []

    def add_validator(self, validator: Validator):
        self.validators.append(validator)

    def validate(self, data: str) -> bool:
        for validator in self.validators:
            if not validator.validate(data):
                return False
        return True


class SecretKeyValidatorHandler(ValidatorHandler):
    def __init__(self):
        super().__init__()
        self.validators.extend(
            [
                secret_key_validator.EmptyStringValidator(),
                secret_key_validator.WrongLengthValidator(),
            ]
        )


class ContentValidatorHandler(ValidatorHandler):
    def __init__(self):
        super().__init__()
        self.validators.extend(
            [
                content_validator.EmptyStringValidator(),
            ]
        )
