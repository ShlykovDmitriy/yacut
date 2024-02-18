from flask import redirect, render_template, flash

from .models import URLMap
from .forms import URLForm
from .utils import get_short_url, check_unique_short_url
from . import app, db


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = URLForm()
    if not form.validate_on_submit():
        return render_template('yacut.html', form=form)
    short = form.short.data
    if not short:
        short = get_short_url()
    if check_unique_short_url(short):
        flash(f'Ссылка {short} - занята!',)
        return render_template('yacut.html', form=form)
    url = URLMap(
        original=form.original.data,
        short=short
    )
    db.session.add(url)
    db.session.commit()
    return render_template('yacut.html', url=url, form=form)


@app.route('/<string:short>')
def short_url_redirect(short):
    return redirect(URLMap.query.filter_by(short=short).first().original)
