from flask_wtf import FlaskForm
from wtforms import SubmitField, URLField
from wtforms.validators import DataRequired, Length, Optional

from .constants import MAX_LEN_SHORT_URL, MIN_LEN_SHORT_URL, MIN_LEN_ORIGINAL_URL, MAX_LEN_ORIGINAL_URL


class URLForm(FlaskForm):
    """Форма для получения ссылок"""
    original_link = URLField(
        'Введите полную ссылку',
        validators=[DataRequired(message='Обязательное поле'),
                    Length(MIN_LEN_ORIGINAL_URL, MAX_LEN_ORIGINAL_URL)]
    )
    custom_id = URLField(
        'Введите короткую ссылку',
        validators=[
            Length(
                MIN_LEN_SHORT_URL,
                MAX_LEN_SHORT_URL,
                message='Длинна короткой ссылки не должна превышать 16 символов'
            ),
            Optional()
        ]
    )
    submit = SubmitField('Создать')
