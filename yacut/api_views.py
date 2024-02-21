import re
from http import HTTPStatus

from flask import jsonify, request

from . import app, db
from .constants import SHORT_URL_REGEX_PATTERN
from .error_handlers import InvalidAPIUsage
from .models import URLMap
from .utils import generation_unique_short_link, get_url_by_short


@app.route('/api/id/<string:short>/', methods=['GET'])
def get_original_url(short):
    """Получение оригинальной ссылки из короткой"""
    short_url = get_url_by_short(short)
    if not short_url:
        raise InvalidAPIUsage('Указанный id не найден', HTTPStatus.NOT_FOUND)
    return jsonify({"url": short_url.original}), HTTPStatus.OK


@app.route('/api/id/', methods=['POST'])
def create_short_url():
    """Создание записи ссылок в БД"""
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
