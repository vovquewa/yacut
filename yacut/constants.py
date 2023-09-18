from string import ascii_letters, digits

ALLOWED_CHARS = ascii_letters + digits
API_REGEX = '^[' + ALLOWED_CHARS + ']+$'
CUSTOM_ID_MAX_LENGTH = 16
ORIGINAL_MAX_LENGTH = 2048
SHORT_LENGTH = 6
REDIRECT_VIEW = 'redirect_view'
MAX_ATTEMPTS = 100
