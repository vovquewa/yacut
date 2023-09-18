from http import HTTPStatus
import re

from flask import abort, jsonify, request, url_for

from . import app
from .constants import REDIRECT_VIEW, API_REGEX, SHORT_MAX_LENGTH
from .error_handlers import InvalidAPIUsage
from .exceptions import AddShortException
from .models import URLMap

ID_NOT_FOUND = 'Указанный id не найден'
BODY_NOT_FOUND = 'Отсутствует тело запроса'
URL_REQUIRED = '"url" является обязательным полем!'
NVALID_SHORT = 'Указано недопустимое имя для короткой ссылки'
NAME_EXISTS = 'Имя "{}" уже занято.'


@app.route('/api/id/<short>/', methods=['GET'])
def get_url(short):
    url_map = URLMap.get(short=short)
    if url_map is None:
        raise InvalidAPIUsage(ID_NOT_FOUND, HTTPStatus.NOT_FOUND)
    return jsonify(
        {
            'url': url_map.original
        }
    ), HTTPStatus.OK


@app.route('/api/id/', methods=['POST'])
def add_url():
    data = request.get_json()
    if not data:
        raise InvalidAPIUsage(BODY_NOT_FOUND)
    if 'url' not in data or not data.get('url'):
        raise InvalidAPIUsage(URL_REQUIRED)
    try:
        short = (
            URLMap.get_unique_short()
            if not data.get('custom_id') else data.get('custom_id')
        )
        if (
            short and
            (
                len(short) > SHORT_MAX_LENGTH or
                not re.match(API_REGEX, short)
            )
        ):
            raise InvalidAPIUsage(NVALID_SHORT)
        if URLMap.get(short=short):
            raise InvalidAPIUsage(
                NAME_EXISTS.format(short)
            )
        url_map = URLMap.add(
            original=data['url'],
            short=short
        )
    except AddShortException as e:
        abort(HTTPStatus.INTERNAL_SERVER_ERROR, str(e))
    return jsonify(
        {
            'url': url_map.original,
            'short_link': url_for(
                REDIRECT_VIEW, short=url_map.short, _external=True
            )
        }
    ), HTTPStatus.CREATED
