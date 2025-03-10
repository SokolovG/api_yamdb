"""Exceptions for user verification service."""


class VerificationError(Exception):
    """Base class for verification service exceptions."""

    default_message = 'Verification error occurred'

    def __init__(self, message: str = None) -> None:
        """Initialize exception with custom or default message."""
        self.message = message or self.default_message
        super().__init__(self.message)


class UsernameEmptyError(VerificationError):
    """Raised when email is empty or None."""

    default_message = 'Username cannot be empty'


class CodeGenerateError(VerificationError):
    """Raised when code generation fails, typically due to Redis errors."""

    default_message = 'Failed to generate the code'


class CodeCleanError(VerificationError):
    """Raised when cleanup of verification codes fails."""

    default_message = 'Failed to clean up verification codes'


class CodeExpiredError(VerificationError):
    """Raised when ttl code expired."""

    default_message = 'The life span of the confirming code has expired.'


class EmailSendError(VerificationError):
    """Raised when an error occurs while sending email via SMTP."""

    default_message = 'Error occurred while sending email'


class CodeNotFoundError(VerificationError):
    """Raised when verification code is not found for given username."""

    default_message = 'Verification code not found'


class InvalidCodeError(VerificationError):
    """Raised when provided verification code does not match stored code."""

    default_message = 'Invalid verification code provided'
