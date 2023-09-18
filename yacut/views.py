from http import HTTPStatus

from flask import abort, flash, redirect, render_template, url_for

from . import app
from .forms import CutForm
from .models import URLMap
from .constants import (
    FLASH_NAME_EXISTS,
    REDIRECT_VIEW,
)
from .exceptions import AddShortException


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = CutForm()
    if URLMap.get(custom_id=form.custom_id.data) is not None:
        flash(
            FLASH_NAME_EXISTS.format(form.custom_id.data)
        )
        return render_template('yacut.html', form=form)
    if form.validate_on_submit():
        try:
            url_map = URLMap.add(
                original=form.original_link.data,
                short=form.custom_id.data or URLMap.get_unique_short_id()
            )
        except AddShortException as e:
            abort(HTTPStatus.INTERNAL_SERVER_ERROR, str(e))
        return render_template(
            'yacut.html',
            form=form,
            short_link=url_for(
                REDIRECT_VIEW,
                short_url=url_map.short,
                _external=True
            )
        )
    return render_template('yacut.html', form=form)


@app.route('/<short_url>')
def redirect_view(short_url):
    url_map = URLMap.get(custom_id=short_url)
    if url_map is None:
        abort(HTTPStatus.NOT_FOUND)
    return redirect(url_map.original)
