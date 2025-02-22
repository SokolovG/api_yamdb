"""Module for custom exceptions for auth logic."""
from users.exceptions.users import (
    VerificationError,
    UsernameEmptyError,
    CodeGenerateError,
    CodeCleanError,
    CodeExpiredError,
    EmailSendError,
    CodeNotFoundError,
    InvalidCodeError
)


__all__ = [
    'VerificationError',
    'UsernameEmptyError',
    'CodeGenerateError',
    'CodeCleanError',
    'CodeExpiredError',
    'EmailSendError',
    'CodeNotFoundError',
    'InvalidCodeError'
]
