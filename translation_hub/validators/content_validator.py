from translation_hub.validators.validator import Validator


class EmptyStringValidator(Validator):
    def validate(self, value: str) -> bool:
        return bool(value)


class FullNumberValidator(Validator):
    def validate(self, value: str) -> bool:
        return value.isnumeric()
