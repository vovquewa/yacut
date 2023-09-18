from datetime import datetime
import re
from random import randrange, choice
from string import ascii_letters, digits

from yacut import db
from .constants import CUSTOM_ID_MAX_LENGTH, ORIGINAL_MAX_LENGTH, API_REGEX, API_INVALID_SHORT, API_NAME_EXISTS, SHORT_LENGTH, MAX_ATTEMPTS, API_SHORT_FAILED
from .error_handlers import InvalidAPIUsage


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
            short_link = ''.join(
                choice(symbols) for _ in range(SHORT_LENGTH)
            )
            if URLMap.get(custom_id=short_link):
                return URLMap.get_unique_short_id()
            return short_link
        raise InvalidAPIUsage(API_SHORT_FAILED)

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
            raise InvalidAPIUsage(API_INVALID_SHORT)

        if URLMap.get(custom_id=short):
            raise InvalidAPIUsage(
                API_NAME_EXISTS.format(short)
            )
        url_map = URLMap(original=original, short=short)
        db.session.add(url_map)
        db.session.commit()
        return url_map
