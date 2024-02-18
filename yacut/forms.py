from flask_wtf import FlaskForm
from wtforms import SubmitField, URLField
from wtforms.validators import DataRequired, Length


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
