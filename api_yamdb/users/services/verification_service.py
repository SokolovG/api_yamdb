"""VerificationService for users.

Contains:
- Generate code
- Send code
- Check code
- Clean cods
"""
from smtplib import SMTPException
from string import digits
from typing import Optional, Final
import secrets

from django.core.mail import send_mail
from redis import Redis
from redis.exceptions import RedisError

from .redis_config import redis_client
from users.constants import (
    CODE_TTL,
    EMAIL_MESSAGE,
    EMAIL_SUBJECT,
    KEY_PREFIX,
    MAX_CONFIRMATION_CODE_LENGTH,
)
from ..exceptions import (
    UsernameEmptyError,
    CodeGenerateError,
    CodeCleanError,
    CodeExpiredError,
    EmailSendError,
    CodeNotFoundError,
    InvalidCodeError
)


class VerificationService:
    """Service for handling user verification through email confirmation codes.

    This service provides functionality for:
    - Generating confirmation codes
    - Sending codes via email
    - Verifying submitted codes
    - Cleaning up expired codes

    The service uses Redis for storing confirmation codes with TTL.
    """

    def __init__(self, redis_client) -> None:
        """Initialize the VerificationService.

        Args:
            redis_client: Redis client instance for storing confirmation codes

        The service is configured with:
        - Code length from MAX_CONFIRMATION_CODE_LENGTH
        - TTL from CODE_TTL
        - Key prefix from KEY_PREFIX
        - Digits for code generation from string.digits
        """
        self._code_length: Final[int] = MAX_CONFIRMATION_CODE_LENGTH
        self._digits: Final[str] = digits
        self._code_ttl: Final[int] = CODE_TTL
        self._key_prefix: Final[str] = KEY_PREFIX
        self._redis: Redis = redis_client

    def generate(self, username: str) -> Optional[str]:
        """Generate confirmation code.

        Args:
            username: str - Username to generate verification code for
        Returns:
            str - Generated confirmation code
        Raises:
            UsernameEmptyError: If username is empty
            CodeGenerateError: If Redis operation fails
        """
        if not username:
            raise UsernameEmptyError()
        try:
            code = ''.join(secrets.choice(self._digits)
                           for _ in range(self._code_length))
            key = f'{self._key_prefix}{username}'
            self._redis.setex(key, self._code_ttl, code)
            return code

        except RedisError as error:
            raise CodeGenerateError() from error

    def send_code(self, email: str, code: str) -> None:
        """Send confirmation code.

        Args:
            email: str - Email address to send code to
            code: str - Verification code to send
        Raises:
            EmailSendError: If sending email fails
        """
        try:
            send_mail(
                subject=EMAIL_SUBJECT,
                message=f'{EMAIL_MESSAGE}{code}',
                from_email='YaReviewApp@example.com',
                recipient_list=[email],
                fail_silently=False
            )
        except SMTPException as error:
            raise EmailSendError() from error

    def _get_valid_key(self, username: str) -> str:
        """Get Redis key for username and verify it's not expired.

        Args:
            username: Username to get key for
        Returns:
            str: Redis key if valid
        Raises:
            CodeExpiredError: If code has expired
            CodeNotFoundError: If code not found
        """
        key = f'{self._key_prefix}{username}'
        ttl = self._redis.ttl(key)

        if ttl == -2:  # Key does not exist
            raise CodeNotFoundError()
        if ttl <= 0:  # Key exists but expired
            raise CodeExpiredError()

        return key

    def check_code(self, code: str, username: str) -> bool:
        """Check confirmation code.

        Args:
            username: str - Username to check code for
            code: str - Verification code to check
        Raises:
            CodeExpiredError: If code has expired
            CodeNotFoundError: If code not found
            InvalidCodeError: If code does not match
        Returns:
            bool - True if code is valid
        """
        # Check TTL.
        key = self._get_valid_key(username)
        stored_code = self._redis.get(key)

        if not stored_code:
            raise CodeNotFoundError()

        if stored_code != code:
            raise InvalidCodeError()

        self._redis.delete(key)
        return True

    def cleanup_old_codes(self, username: str) -> None:
        """Clean up verification codes for the given username.

        Removes any existing verification codes from Redis storage
        for the specified username.

        Args:
            username: Username to clean up codes for
        Raises:
            CodeCleanError: If Redis operation fails
        """
        try:
            key = f'{self._key_prefix}{username}'
            result = self._redis.delete(key)
            if result is None:
                raise CodeCleanError("Redis operation failed")
        except RedisError as error:
            raise CodeCleanError() from error


verification_service = VerificationService(redis_client)
