from flask import abort, flash, redirect, render_template, request

from . import app
from .error_handlers import InvalidData
from .forms import URLForm
from .models import URLMap
from .services import ShortUrlService

short_url_service = ShortUrlService()


@app.route('/', methods=['GET', 'POST'])
def index_view():
    """Функция главной страницы."""
    form = URLForm()
    if not form.validate_on_submit():
        return render_template('yacut.html', form=form)
    try:
        url_map = short_url_service.create_short_url(
            form.original_link.data, form.custom_id.data)
        flash(f'Короткая ссылка: '
              f'<a href="{request.base_url}{url_map.short}">'
              f'{request.base_url}{url_map.short}</a>')
        return render_template('yacut.html', url=url_map, form=form)
    except InvalidData as e:
        flash(str(e.message))
        return render_template('yacut.html', form=form)


@app.route('/<string:short>')
def short_url_redirect(short):
    """Функция перенаправляет на оригинальную страницу"""
    short_url = URLMap.get_url_by_short(short)
    if not short_url:
        abort(404)
    return redirect(short_url.original)
