from rest_framework.validators import UniqueValidator

from users.models import User
from users.constants import EMAIL_NOT_UNIQUE_MSG, USERNAME_NOT_UNIQUE_MSG



email_validator = UniqueValidator(
    queryset=User.objects.all().only('email'),
    message=EMAIL_NOT_UNIQUE_MSG,
    lookup='iexact'
)

username_validator = UniqueValidator(
    queryset=User.objects.all().only('username'),
    message=USERNAME_NOT_UNIQUE_MSG,
    lookup='iexact'
)