import re
from datetime import datetime
from random import choice
from string import ascii_letters, digits

from yacut import db

from .constants import (API_REGEX, CUSTOM_ID_MAX_LENGTH, MAX_ATTEMPTS,
                        ORIGINAL_MAX_LENGTH, SHORT_LENGTH)
from .error_handlers import InvalidAPIUsage

NVALID_SHORT = 'Указано недопустимое имя для короткой ссылки'
SHORT_FAILED = 'Не удалось сгенерировать уникальный id'
NAME_EXISTS = 'Имя "{}" уже занято.'


class URLMap(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.String(ORIGINAL_MAX_LENGTH), nullable=False)
    short = db.Column(
        db.String(CUSTOM_ID_MAX_LENGTH), nullable=False, unique=True
    )
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def get_unique_short_id(attempts=0):
        if attempts <= MAX_ATTEMPTS:
            symbols = ascii_letters + digits
            short = ''.join(
                choice(symbols) for _ in range(SHORT_LENGTH)
            )
            if URLMap.get(custom_id=short):
                return URLMap.get_unique_short_id()
            return short
        raise InvalidAPIUsage(SHORT_FAILED)

    def get(custom_id):
        return URLMap.query.filter_by(short=custom_id).first()

    def add(original, short):
        regex = API_REGEX
        if (
            short and
            (
                len(short) > CUSTOM_ID_MAX_LENGTH or
                not bool(re.match(regex, short))
            )
        ):
            raise InvalidAPIUsage(NVALID_SHORT)

        if URLMap.get(custom_id=short):
            raise InvalidAPIUsage(
                NAME_EXISTS.format(short)
            )
        url_map = URLMap(original=original, short=short)
        db.session.add(url_map)
        db.session.commit()
        return url_map
