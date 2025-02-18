"""Exceptions for user verification service."""


class VerificationError(Exception):
    """Base class for verification service exceptions."""

    default_message = 'Verification error occurred'

    def __init__(self, message: str = None) -> None:
        """Initialize exception with custom or default message."""
        self.message = message or self.default_message
        super().__init__(self.message)

    """Base exception for verification service errors."""


class EmailEmptyError(VerificationError):
    """Raised when email is empty or None."""

    default_message = 'Email cannot be empty'


class CodeGenerateError(VerificationError):
    """Raised when code generation fails, typically due to Redis errors."""

    default_message = 'Failed to generate the code'


class CodeCleanError(VerificationError):
    """Raised when cleanup of verification codes fails."""

    default_message = 'Failed to clean up verification codes'
