from http import HTTPStatus

from flask import abort, flash, redirect, render_template, url_for

from . import app
from .constants import REDIRECT_VIEW
from .forms import CutForm
from .models import URLMap
from .error_handlers import InvalidURLMap

NAME_EXISTS = 'Имя {} уже занято!'


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = CutForm()
    if not form.validate_on_submit():
        return render_template('index.html', form=form)
    try:
        return render_template(
            'index.html',
            form=form,
            short_link=url_for(
                REDIRECT_VIEW,
                short=URLMap.add(
                    original=form.original_link.data,
                    short=form.custom_id.data
                ).short,
                _external=True
            ),
            additional_validation=True
        )
    except InvalidURLMap as e:
        flash(e)
        return render_template('index.html', form=form)


@app.route('/<short>')
def redirect_view(short):
    url_map = URLMap.get(short=short)
    if url_map is None:
        abort(HTTPStatus.NOT_FOUND)
    return redirect(url_map.original)
