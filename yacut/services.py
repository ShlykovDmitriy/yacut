import random
import re
import string as s

from . import db
from .constants import LEN_SHORT_URL_AUTO, SHORT_URL_REGEX_PATTERN
from .error_handlers import InvalidData
from .models import URLMap


class ShortUrlService:
    """Сервис для работы с короткими ссылками"""

    def __init__(self):
        self.short_url = None

    def _generate_unique_short_link(self):
        """Создание уникальной короткой ссылки"""
        while True:
            short = ''.join(
                random.choice(
                    s.ascii_letters + s.digits
                ) for i in range(LEN_SHORT_URL_AUTO)
            )
            if not URLMap.get_url_by_short(short):
                return short

    def _validate_short_url(self):
        """Создает короткую ссылку или валидирует ее при наличии."""
        if URLMap.get_url_by_short(self.short_url):
            raise InvalidData(
                'Предложенный вариант короткой ссылки уже существует.')
        elif not re.match(SHORT_URL_REGEX_PATTERN, self.short_url):
            raise InvalidData('Указано недопустимое имя для короткой ссылки')

    def create_short_url(self, url, short: None):
        """Создает запись в БД"""
        self.short_url = short if short else self._generate_unique_short_link()
        self._validate_short_url()
        url_map = URLMap()
        url_map.from_dict({'url': url, 'custom_id': self.short_url})
        db.session.add(url_map)
        db.session.commit()
        return url_map
