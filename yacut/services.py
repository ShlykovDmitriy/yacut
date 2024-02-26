import random
import re
import string as s

from . import db
from .constants import LEN_SHORT_URL_AUTO, SHORT_URL_REGEX_PATTERN
from .error_handlers import InvalidData
from .models import URLMap


class ShortUrlService:
    """Сервис для работы с короткими ссылками"""

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

    def _validate_short_url(self, short):
        """Создает которкую ссылку или валидирует ее при наличии."""
        if not short:
            short = self._generate_unique_short_link()
        elif URLMap.get_url_by_short(short):
            raise InvalidData(
                'Предложенный вариант короткой ссылки уже существует.')
        elif not re.match(SHORT_URL_REGEX_PATTERN, short):
            raise InvalidData('Указано недопустимое имя для короткой ссылки')
        return short

    def create_short_url(self, url, short):
        """Создает запись в БД"""
        short = self._validate_short_url(short)
        url_map = URLMap()
        url_map.from_dict({'url': url, 'custom_id': short})
        db.session.add(url_map)
        db.session.commit()
        return url_map
