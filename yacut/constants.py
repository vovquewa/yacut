from string import ascii_letters, digits

FLASH_NAME_EXISTS = 'Имя {} уже занято!'
FLASH_SUCCESS = 'Ваша новая ссылка готова:'


API_INVALID_SHORT = 'Указано недопустимое имя для короткой ссылки'
API_SHORT_FAILED = 'Не удалось сгенерировать уникальный id'
API_NAME_EXISTS = 'Имя "{}" уже занято.'
ALLOWED_CHARS = ascii_letters + digits
API_REGEX = '^[' + ALLOWED_CHARS + ']+$'

CUSTOM_ID_MAX_LENGTH = 16
ORIGINAL_MAX_LENGTH = 2048
SHORT_LENGTH = 6

REDIRECT_VIEW = 'redirect_view'

MAX_ATTEMPTS = 100
