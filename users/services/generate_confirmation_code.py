import secrets
from string import digits

from ..constants import MAX_CONFIRMATION_CODE_LENGTH

class GenerateConfirmationCode:

    def __init__(self) -> None:
        self._code_length = MAX_CONFIRMATION_CODE_LENGTH
        self._digits = digits

    def generate(self) -> str:
        code = ''.join(secrets.choice(self._digits) for _ in range(self._code_length))
        return code


code_generator = GenerateConfirmationCode()