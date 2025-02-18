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


class VerificationService:
    def __init__(self, redis_client) -> None:
        self._code_length: int = MAX_CONFIRMATION_CODE_LENGTH
        self._digits: str = digits
        self._code_ttl: int = CODE_TTL
        self._key_prefix: str = KEY_PREFIX
        self._redis: Redis = redis_client

    def generate(self, email: str) -> Optional[str]:
        if not email:
            raise  ValueError('Email cannot be empty')
        try:
            code = ''.join(secrets.choice(self._digits) for _ in range(self._code_length))
            key = f'{self._key_prefix}{email}'
            self._redis.setex(key, self._code_ttl, code)
            return code

        except RedisError as e:
            raise ValueError('Failed to generate the code.') from e


    def send_code(self, email: str) -> None:
        code = self.generate(email)
        if not code:
            raise ValueError('Failed to generate code')
        send_mail(
            subject=EMAIL_SUBJECT,
            message=f'{EMAIL_MESSAGE}{code}',
            from_email='YaReviewApp@example.com',
            recipient_list=[email],
            fail_silently=False
        )

    def check_code(self, email: str, code: str) -> bool:
        key = f'{self._key_prefix}{email}'
        stored_code = self._redis.get(key)

        if not stored_code:
            return False

        if stored_code == code:
            self._redis.delete(key)
            return True

    def cleanup_old_codes(self, email: str) -> None:
        try:
            key = f'{self._key_prefix}{email}'
            self._redis.delete(key)
        except RedisError as e:
            raise ValueError("Failed to cleanup verification codes") from e

verification_service = VerificationService(redis_client)