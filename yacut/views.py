from http import HTTPStatus
from random import randrange

from flask import abort, flash, redirect, render_template, url_for

from . import app, db
from .forms import CutForm
from .models import URLMap
from .constants import (
    FLASH_NAME_EXISTS,
    FLASH_SUCCESS,
    UNIQUE_ID_LENGTH
)


def get_unique_short_id():
    """Генерирует короткую ссылку.
    - Состоит из 6 символов.
    - Символы берутся из набора [a-zA-Z0-9].
    """
    symbols = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
    short_link = ''
    for i in range(UNIQUE_ID_LENGTH):
        short_link += symbols[randrange(len(symbols))]
    if URLMap.query.filter_by(short=short_link).first():
        return get_unique_short_id()
    return short_link


@app.route('/', methods=['GET', 'POST'])
def index_view():
    try:
        form = CutForm()
        if form.validate_on_submit():
            if URLMap.query.filter_by(short=form.custom_id.data).first():
                flash(
                    FLASH_NAME_EXISTS.format(form.custom_id.data),
                    'short_exists'
                )
                return render_template('yacut.html', form=form)
            url_map = URLMap(
                original=form.original_link.data,
                short=form.custom_id.data or get_unique_short_id()
            )
            db.session.add(url_map)
            db.session.commit()
            flash(FLASH_SUCCESS, 'success_message')
            return render_template(
                'yacut.html',
                form=form,
                short_link=url_for(
                    'redirect_view',
                    short_url=url_map.short,
                    _external=True
                )
            )
        return render_template('yacut.html', form=form)
    except Exception:
        abort(HTTPStatus.INTERNAL_SERVER_ERROR)


@app.route('/<short_url>')
def redirect_view(short_url):
    url_map = URLMap.query.filter_by(short=short_url).first()
    if url_map is None:
        abort(HTTPStatus.NOT_FOUND)
    return redirect(url_map.original)
