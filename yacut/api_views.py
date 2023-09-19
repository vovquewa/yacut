from http import HTTPStatus

from flask import jsonify, request, url_for

from . import app
from .constants import REDIRECT_VIEW
from .error_handlers import InvalidAPIUsage, InvalidURLMap
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
        url_map = URLMap.add(
            original=data['url'],
            short=data.get('custom_id')
        )
    except InvalidURLMap as e:
        raise InvalidAPIUsage(str(e))
    return jsonify(
        {
            'url': data['url'],
            'short_link': url_for(
                REDIRECT_VIEW, short=url_map.short, _external=True
            )
        }
    ), HTTPStatus.CREATED
