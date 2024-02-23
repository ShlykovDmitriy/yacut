from flask import abort, flash, redirect, render_template, request

from . import app, db
from .error_handlers import InvalidData
from .forms import URLForm
from .models import URLMap
from .utils import (get_url_by_short, save_in_db, validation_short_url)


@app.route('/', methods=['GET', 'POST'])
def index_view():
    """Функция главной страницы."""
    form = URLForm()
    if not form.validate_on_submit():
        return render_template('yacut.html', form=form)
    url = URLMap()
    try:
        short_link = validation_short_url(form.custom_id.data)
        url = URLMap(
            original=form.original_link.data,
            short=short_link
        )
        save_in_db(db, url)
        flash(f'Короткая ссылка: '
              f'<a href="{request.base_url}{short_link}">{request.base_url}{short_link}</a>')
        return render_template('yacut.html', url=url, form=form)
    except InvalidData as e:
        flash(str(e.message))
        return render_template('yacut.html', url=url, form=form)


@app.route('/<string:short>')
def short_url_redirect(short):
    """Функция перенаправляет на оригинальную страницу"""
    short_url = get_url_by_short(short)
    if not short_url:
        abort(404)
    return redirect(short_url.original)
