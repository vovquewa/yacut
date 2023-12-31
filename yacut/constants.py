from string import ascii_letters, digits
import re

ALLOWED_CHARS = ascii_letters + digits
API_REGEX = f'^[{re.escape(ALLOWED_CHARS)}]+$'
SHORT_MAX_LENGTH = 16
ORIGINAL_MAX_LENGTH = 2048
SHORT_LENGTH = 6
REDIRECT_VIEW = 'redirect_view'
MAX_ATTEMPTS = 10
