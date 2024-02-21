import random
import string as s

from .constants import LEN_SHORT_URL_AUTO
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


def sd(data):
    data = request.get_json()
    if not data:
        raise InvalidAPIUsage('Отсутствует тело запроса')
    if 'url' not in data:
        raise InvalidAPIUsage('\"url\" является обязательным полем!')
    if not data.get('custom_id'):
        data['custom_id'] = generation_unique_short_link()
    elif get_url_by_short(data['custom_id']):
        raise InvalidAPIUsage('Предложенный вариант короткой ссылки уже существует.')
    elif not re.match(SHORT_URL_REGEX_PATTERN, data['custom_id']):
        raise InvalidAPIUsage('Указано недопустимое имя для короткой ссылки')
    url_map = URLMap()
    url_map.from_dict(data)
    db.session.add(url_map)
    db.session.commit()
    return jsonify(url_map.to_dict()), HTTPStatus.CREATED