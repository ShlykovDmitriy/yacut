import random
import re
import string as s

from .constants import LEN_SHORT_URL_AUTO, SHORT_URL_REGEX_PATTERN
from .error_handlers import InvalidData
from .models import URLMap


def generation_unique_short_link():
    """Создание короткой ссылки"""
    short = ''.join(random.choice(s.ascii_letters + s.digits) for i in range(LEN_SHORT_URL_AUTO))
    if not get_url_by_short(short):
        return short
    return generation_unique_short_link()


def get_url_by_short(short):
    """Проверка на уникальность короткой ссылки"""
    return URLMap.query.filter_by(short=short).first()


def validation_short_url(short: None):
    if not short:
        short = generation_unique_short_link()
    elif get_url_by_short(short):
        raise InvalidData('Предложенный вариант короткой ссылки уже существует.')
    elif not re.match(SHORT_URL_REGEX_PATTERN, short):
        raise InvalidData('Указано недопустимое имя для короткой ссылки')
    return short


def validation_api(data):
    if not data:
        raise InvalidData('Отсутствует тело запроса')
    if 'url' not in data:
        raise InvalidData('\"url\" является обязательным полем!')
    data['custom_id'] = validation_short_url(data.get('custom_id'))
    return data


def save_in_db(db, url):
    db.session.add(url)
    db.session.commit()
