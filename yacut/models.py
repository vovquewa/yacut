from datetime import datetime
import re

from yacut import db
from .constants import CUSTOM_ID_MAX_LENGTH, ORIGINAL_MAX_LENGTH, API_REGEX, API_INVALID_SHORT, API_NAME_EXISTS
from .error_handlers import InvalidAPIUsage


class URLMap(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.String(ORIGINAL_MAX_LENGTH), nullable=False)
    short = db.Column(
        db.String(CUSTOM_ID_MAX_LENGTH), nullable=False, unique=True
    )
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

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