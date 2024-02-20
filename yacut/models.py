from datetime import datetime

from flask import url_for

from . import db
from .constants import MAX_LEN_SHORT_URL, MAX_LEN_ORIGINAL_URL


class URLMap(db.Model):
    """Модель для работы с ссылками"""
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.String(MAX_LEN_ORIGINAL_URL), nullable=False)
    short = db.Column(db.String(MAX_LEN_SHORT_URL), nullable=False)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def to_dict(self):
        """Метод конвертации объекта в словарь"""
        return dict(
            url=self.original,
            short_link=url_for('short_url_redirect',
                               short=self.short,
                               _external=True))

    def from_dict(self, data):
        """Метод конвертации словаря в объект"""
        setattr(self, 'original', data['url'])
        setattr(self, 'short', data['custom_id'])
