from datetime import datetime

from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import SubmitField, URLField
from wtforms.validators import DataRequired, Length

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'MY SECRET KEY'

db = SQLAlchemy(app)


class URLMap(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.String(128), nullable=False)
    short = db.Column(db.String(16), nullable=False)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)


class URLForm(FlaskForm):
    original = URLField(
        'Введите полную ссылку',
        validators=[DataRequired(message='Обязательное поле'),
                    Length(1, 128)]
    )
    short = URLField(
        'Введите короткую ссылку',
        validators=[Length(1, 16, message='Длинна короткой ссылки не должна превышать 16 символов')]
    )
    submit = SubmitField('Создать')


@app.route('/')
def index_view():
    form = URLForm
    return render_template('yacut.html', form=form)


if __name__ == '__main__':
    app.run()
