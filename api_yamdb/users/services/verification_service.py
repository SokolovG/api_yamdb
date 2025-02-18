"""VerificationService for users.

Contains:
- Generate code
- Send code
- Check code
- Clean cods
"""
from string import digits
from typing import Optional
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
from ..exceptions import EmailEmptyError, CodeGenerateError, CodeCleanError


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
        self._code_length: int = MAX_CONFIRMATION_CODE_LENGTH
        self._digits: str = digits
        self._code_ttl: int = CODE_TTL
        self._key_prefix: str = KEY_PREFIX
        self._redis: Redis = redis_client

    def generate(self, email: str) -> Optional[str]:
        """Generate confirmation code.

        Args:
            email
        Returns:
            Code or ValueError
        """
        if not email:
            raise EmailEmptyError()
        try:
            code = ''.join(secrets.choice(self._digits)
                           for _ in range(self._code_length))
            key = f'{self._key_prefix}{email}'
            self._redis.setex(key, self._code_ttl, code)
            return code

        except RedisError as e:
            raise CodeGenerateError from e

    def send_code(self, email: str) -> None:
        """Send confirmation code.

        Args:
            email
        Returns:
            None
        """
        code = self.generate(email)
        if not code:
            raise CodeGenerateError

        send_mail(
            subject=EMAIL_SUBJECT,
            message=f'{EMAIL_MESSAGE}{code}',
            from_email='YaReviewApp@example.com',
            recipient_list=[email],
            fail_silently=False
        )

    def check_code(self, email: str, code: str) -> bool:
        """Check confirmation code.

        Args:
            email
            code
        Returns:
            True or False
        """
        key = f'{self._key_prefix}{email}'
        stored_code = self._redis.get(key)

        if not stored_code:
            return False

        if stored_code == code:
            self._redis.delete(key)
            return True

    def cleanup_old_codes(self, email: str) -> None:
        """Send confirmation code.

        Args:
            email
        Returns:
            None
        """
        try:
            key = f'{self._key_prefix}{email}'
            self._redis.delete(key)
        except RedisError as e:
            raise CodeCleanError from e


verification_service = VerificationService(redis_client)
