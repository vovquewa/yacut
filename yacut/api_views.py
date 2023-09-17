import re
from http import HTTPStatus

from flask import jsonify, request, url_for

from . import app, db
from .constants import (API_BODY_NOT_FOUND, API_ID_NOT_FOUND,
                        API_INVALID_SHORT, API_NAME_EXISTS, API_PATTERN,
                        API_URL_REQUIRED, CUSTOM_ID_MAX_LENGTH)
from .error_handlers import InvalidAPIUsage
from .models import URLMap
from .views import get_unique_short_id


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
    pattern = re.compile(API_PATTERN)
    data = request.get_json()
    if not data:
        raise InvalidAPIUsage(API_BODY_NOT_FOUND)
    if 'url' not in data or not data.get('url'):
        raise InvalidAPIUsage(API_URL_REQUIRED)
    if (
        data.get('custom_id') and
        len(data.get('custom_id')) > CUSTOM_ID_MAX_LENGTH
    ) \
            or (
                data.get('custom_id') and
                not pattern.match(data.get('custom_id'))
    ):
        raise InvalidAPIUsage(API_INVALID_SHORT)
    if (data.get('custom_id') and not pattern.match(data.get('custom_id'))):
        raise InvalidAPIUsage(API_INVALID_SHORT)
    if URLMap.get(custom_id=data.get('custom_id')):
        raise InvalidAPIUsage(
            API_NAME_EXISTS.format(data.get('custom_id'))
        )
    short_url = (
        get_unique_short_id()
        if not data.get('custom_id') else data.get('custom_id')
    )
    url_map = URLMap(
        original=data['url'],
        short=short_url
    )

    db.session.add(url_map)
    db.session.commit()

    return jsonify(
        {
            'url': url_map.original,
            'short_link': url_for(
                'redirect_view', short_url=short_url, _external=True
            )
        }
    ), HTTPStatus.CREATED
