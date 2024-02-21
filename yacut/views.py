from flask import abort, flash, redirect, render_template, request

from . import app, db
from .forms import URLForm
from .models import URLMap
from .utils import get_url_by_short, generation_unique_short_link


@app.route('/', methods=['GET', 'POST'])
def index_view():
    """Функция главной страницы."""
    form = URLForm()
    if not form.validate_on_submit():
        return render_template('yacut.html', form=form)
    short = form.custom_id.data
    if not short:
        short = generation_unique_short_link()
    if get_url_by_short(short):
        flash('Предложенный вариант короткой ссылки уже существует.',)
        return render_template('yacut.html', form=form)
    url = URLMap(
        original=form.original_link.data,
        short=short
    )
    db.session.add(url)
    db.session.commit()
    flash(f'Короткая ссылка: '
          f'<a href="{request.base_url}{short}">{request.base_url}{short}</a>')
    return render_template('yacut.html', url=url, form=form)


@app.route('/<string:short>')
def short_url_redirect(short):
    """Функция перенаправляет на оригинальную страницу"""
    short_url = get_url_by_short(short)
    if not short_url:
        abort(404)
    return redirect(short_url.original)
