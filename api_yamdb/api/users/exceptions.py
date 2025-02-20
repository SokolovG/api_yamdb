from rest_framework.exceptions import APIException
from rest_framework import status

from rest_framework import serializers


class UserNotFoundException(APIException):
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = "User not found"


class ConfirmationCodeExpired(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'Code has expired'


class ConfirmationCodeInvalid(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'Invalid confirmation code'
