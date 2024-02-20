import random
import string as s

from .constants import LEN_SHORT_URL_AUTO
from .models import URLMap


def get_short_url():
    """Создание короткой ссылки"""
    short = ''.join(random.choice(s.ascii_letters + s.digits) for i in range(LEN_SHORT_URL_AUTO))
    if not check_unique_short_url(short):
        return short
    return get_short_url()


def check_unique_short_url(short):
    """Проверка на уникальность короткой ссылки"""
    return URLMap.query.filter_by(short=short).first()
