from rest_framework.validators import ValidationError

from users.constants import MAX_CONFIRMATION_CODE_LENGTH


class ConfirmationCodeValidator:
    def __init__(self, length: int = MAX_CONFIRMATION_CODE_LENGTH) -> None:
        self.length = length

    def __call__(self, code: str) -> None:
        if not code.isdigit():
            raise ValidationError('The code must contain only numbers.')
        if len(code) != self.length:
            raise ValidationError('The code must contain 6 numbers.')