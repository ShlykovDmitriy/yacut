import random
import re
import string as s

from .constants import LEN_SHORT_URL_AUTO, SHORT_URL_REGEX_PATTERN
from .error_handlers import InvalidData
from .models import URLMap


class ShortUrlService:
    """Сервис для работы с короткими ссылками"""

    def generate_unique_short_link(self):
        """Создание уникальной короткой ссылки"""
        while True:
            short = ''.join(random.choice(s.ascii_letters + s.digits) for i in range(LEN_SHORT_URL_AUTO))
            if not self.get_url_by_short(short):
                return short

    def get_url_by_short(self, short):
        """Проверка наличия короткой ссылки в базе данных"""
        return URLMap.query.filter_by(short=short).first()

    def create_or_validate_short_url(self, short):
        """Создает которкую ссылку или валидирует ее при наличии."""
        if not short:
            short = self.generate_unique_short_link()
        elif self.get_url_by_short(short):
            raise InvalidData('Предложенный вариант короткой ссылки уже существует.')
        elif not re.match(SHORT_URL_REGEX_PATTERN, short):
            raise InvalidData('Указано недопустимое имя для короткой ссылки')
        return short


def save_in_db(db, url):
    """Создает запись в БД"""
    db.session.add(url)
    db.session.commit()
