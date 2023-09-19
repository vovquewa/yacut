from datetime import datetime
import random

from yacut import db

from .constants import (
    ALLOWED_CHARS, SHORT_MAX_LENGTH, MAX_ATTEMPTS,
    ORIGINAL_MAX_LENGTH, SHORT_LENGTH
)
from .error_handlers import InvalidAPIUsage

SHORT_FAILED = 'Не удалось сгенерировать уникальный id'
SHORT_UNACCEPTABLE = 'Указано недопустимое имя для короткой ссылки'


class URLMap(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.String(ORIGINAL_MAX_LENGTH), nullable=False)
    short = db.Column(
        db.String(SHORT_MAX_LENGTH), nullable=False, unique=True
    )
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def get_unique_short():
        for _ in range(MAX_ATTEMPTS):
            short = ''.join(random.choices(ALLOWED_CHARS, k=SHORT_LENGTH))
            if not URLMap.get(short=short):
                return short
        raise InvalidAPIUsage(SHORT_FAILED)

    def get(short):
        return URLMap.query.filter_by(short=short).first()

    def add(original, short=None):
        if short is None or short == '':
            short = URLMap.get_unique_short()
        if len(short) > SHORT_MAX_LENGTH:
            raise InvalidAPIUsage(SHORT_UNACCEPTABLE)
        url_map = URLMap(original=original, short=short)
        db.session.add(url_map)
        db.session.commit()
        return url_map
