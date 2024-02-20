from flask_wtf import FlaskForm
from wtforms import SubmitField, URLField
from wtforms.validators import DataRequired, Length, Optional


class URLForm(FlaskForm):
    original_link = URLField(
        'Введите полную ссылку',
        validators=[DataRequired(message='Обязательное поле'),
                    Length(1, 128)]
    )
    custom_id = URLField(
        'Введите короткую ссылку',
        validators=[Length(1, 16, message='Длинна короткой ссылки не должна превышать 16 символов'), Optional()]
    )
    submit = SubmitField('Создать')
