from flask import abort, flash, redirect, render_template, request

from . import app, db
from .forms import URLForm
from .models import URLMap
from .utils import check_unique_short_url, get_short_url


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = URLForm()
    if not form.validate_on_submit():
        return render_template('yacut.html', form=form)
    short = form.custom_id.data
    if not short:
        short = get_short_url()
    if check_unique_short_url(short):
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
    short_url = URLMap.query.filter_by(short=short).first()
    if not short_url:
        abort(404)
    return redirect(short_url.original)
