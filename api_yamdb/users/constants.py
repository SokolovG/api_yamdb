"""Main constants file for users app."""
MAX_EMAIL_LENGTH = 254
MAX_ROLE_LENGTH = 20
MAX_CONFIRMATION_CODE_LENGTH = 6

EMAIL_SUBJECT = 'Confirm account'
EMAIL_MESSAGE = 'Please confirm your account with code: '

CODE_TTL = 300
KEY_PREFIX = 'verification:code:'

NOT_UNIQUE_MSG = 'already exists in the system. Please try another one.'
EMAIL_NOT_UNIQUE_MSG = f'E - mail address {NOT_UNIQUE_MSG}'
USERNAME_NOT_UNIQUE_MSG = f'Username {NOT_UNIQUE_MSG}'