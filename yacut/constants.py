from string import ascii_letters, digits

FLASH_NAME_EXISTS = 'Имя {} уже занято!'
FLASH_SUCCESS = 'Ваша новая ссылка готова:'

FORMS_LONG_LINK = 'Длинная ссылка'
FORMS_REQUIRED = 'Обязательное поле'
FORMS_YOUR_SHORT_LINK = 'Ваш вариант короткой ссылки'
FORMS_SHORT_LINK_VALIDATION = 'Короткая ссылка может быть не более 16 символов'
FORMS_CREATE = 'Создать'

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
