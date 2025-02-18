from django.core.exceptions import ValidationError
from django.utils import timezone

from .constants import FIRST_YEAR_OF_MOVIES


def validate_year(value) -> bool:
    if value > timezone.now().year:
        raise ValidationError(
            f'Год {value} из будующего!',
            params={'value': value},
        )
    if value < FIRST_YEAR_OF_MOVIES:
        raise ValidationError(
            f'Год {value} меньше первого года кинематографа!',
            params={'value': value},
        )
