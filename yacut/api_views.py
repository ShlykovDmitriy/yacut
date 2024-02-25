from http import HTTPStatus

from flask import jsonify, request

from . import app, db
from .error_handlers import InvalidData
from .models import URLMap
from .utils import ShortUrlService, save_in_db

short_url_service = ShortUrlService()


@app.route('/api/id/<string:short>/', methods=['GET'])
def get_original_url(short):
    """Получение оригинальной ссылки из короткой"""
    short_url = short_url_service.get_url_by_short(short)
    if not short_url:
        raise InvalidData('Указанный id не найден', HTTPStatus.NOT_FOUND)
    return jsonify({"url": short_url.original}), HTTPStatus.OK


@app.route('/api/id/', methods=['POST'])
def create_short_url():
    """Создание записи ссылок в БД"""
    data = request.get_json()
    if not data:
        raise InvalidData('Отсутствует тело запроса')
    if 'url' not in data:
        raise InvalidData('\"url\" является обязательным полем!')
    data['custom_id'] = short_url_service.create_or_validate_short_url(data.get('custom_id'))
    url_map = URLMap()
    url_map.from_dict(data)
    save_in_db(db, url_map)
    return jsonify(url_map.to_dict()), HTTPStatus.CREATED