"""Custom validators.

Contains:
- username_validator
= ConfirmationCodeValidator
"""
from django.core.validators import RegexValidator
from rest_framework.validators import ValidationError

from users.constants import MAX_CONFIRMATION_CODE_LENGTH


username_validator = RegexValidator(
    regex=r'^[\w.@+-]+\Z',
    message='Enter a valid username. This value may contain only letters, '
            'numbers, and @/./+/-/_ characters.'
)


class ConfirmationCodeValidator:
    """Validate code from user."""

    def __init__(self, length: int = MAX_CONFIRMATION_CODE_LENGTH) -> None:
        """Use 6 digits as the default code length."""
        self.length = length

    def __call__(self, code: str) -> None:
        """Call when creating class instance."""
        if not code.isdigit():
            raise ValidationError('The code must contain only numbers.')
        if len(code) != self.length:
            raise ValidationError('The code must contain 6 numbers.')
