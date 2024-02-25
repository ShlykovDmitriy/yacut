from flask import abort, flash, redirect, render_template, request

from . import app, db
from .error_handlers import InvalidData
from .forms import URLForm
from .models import URLMap
from .utils import ShortUrlService, save_in_db

short_url_service = ShortUrlService()


@app.route('/', methods=['GET', 'POST'])
def index_view():
    """Функция главной страницы."""
    form = URLForm()
    if not form.validate_on_submit():
        return render_template('yacut.html', form=form)
    url = URLMap()
    try:
        short = short_url_service.create_or_validate_short_url(form.custom_id.data)
        url = URLMap(
            original=form.original_link.data,
            short=short
        )
        save_in_db(db, url)
        flash(f'Короткая ссылка: '
              f'<a href="{request.base_url}{short}">{request.base_url}{short}</a>')
        return render_template('yacut.html', url=url, form=form)
    except InvalidData as e:
        flash(str(e.message))
        return render_template('yacut.html', url=url, form=form)


@app.route('/<string:short>')
def short_url_redirect(short):
    """Функция перенаправляет на оригинальную страницу"""
    short_url = short_url_service.get_url_by_short(short)
    if not short_url:
        abort(404)
    return redirect(short_url.original)
