import re
from http import HTTPStatus

from flask import jsonify, request, url_for

from . import app, db
from .constants import (REDIRECT_VIEW,)
from .error_handlers import InvalidAPIUsage
from .models import URLMap
from .views import get_unique_short_id


API_ID_NOT_FOUND = 'Указанный id не найден'
API_BODY_NOT_FOUND = 'Отсутствует тело запроса'
API_URL_REQUIRED = '"url" является обязательным полем!'


@app.route('/api/id/<short_url>/', methods=['GET'])
def get_url(short_url):
    url_map = URLMap.query.filter_by(short=short_url).first()
    if url_map is None:
        raise InvalidAPIUsage(API_ID_NOT_FOUND, HTTPStatus.NOT_FOUND)
    return jsonify(
        {
            'url': url_map.original
        }
    ), HTTPStatus.OK


@app.route('/api/id/', methods=['POST'])
def add_url():
    data = request.get_json()
    if not data:
        raise InvalidAPIUsage(API_BODY_NOT_FOUND)
    if 'url' not in data or not data.get('url'):
        raise InvalidAPIUsage(API_URL_REQUIRED)
    short_url = (
        get_unique_short_id()
        if not data.get('custom_id') else data.get('custom_id')
    )
    url_map = URLMap.add(
        original=data['url'],
        short=short_url
    )
    return jsonify(
        {
            'url': url_map.original,
            'short_link': url_for(
                REDIRECT_VIEW, short_url=short_url, _external=True
            )
        }
    ), HTTPStatus.CREATED