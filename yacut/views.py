from http import HTTPStatus

from flask import abort, redirect, render_template, url_for

from . import app
from .constants import REDIRECT_VIEW
from .exceptions import AddShortException
from .forms import CutForm
from .models import URLMap

NAME_EXISTS = 'Имя {} уже занято!'


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = CutForm()
    if not form.validate_on_submit():
        return render_template('index.html', form=form)
    try:
        url_map = URLMap.add(
            original=form.original_link.data,
            short=form.custom_id.data
        )
    except AddShortException as e:
        abort(HTTPStatus.INTERNAL_SERVER_ERROR, str(e))
    return render_template(
        'index.html',
        form=form,
        short_link=url_for(
            REDIRECT_VIEW,
            short=url_map.short,
            _external=True
        )
    )


@app.route('/<short>')
def redirect_view(short):
    url_map = URLMap.get(short=short)
    if url_map is None:
        abort(HTTPStatus.NOT_FOUND)
    return redirect(url_map.original)
