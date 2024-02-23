from http import HTTPStatus

from flask import jsonify, request

from . import app, db
from .error_handlers import InvalidData
from .models import URLMap
from .utils import get_url_by_short, save_in_db, validation_api


@app.route('/api/id/<string:short>/', methods=['GET'])
def get_original_url(short):
    """Получение оригинальной ссылки из короткой"""
    short_url = get_url_by_short(short)
    if not short_url:
        raise InvalidData('Указанный id не найден', HTTPStatus.NOT_FOUND)
    return jsonify({"url": short_url.original}), HTTPStatus.OK


@app.route('/api/id/', methods=['POST'])
def create_short_url():
    """Создание записи ссылок в БД"""
    data = request.get_json()
    url_map = URLMap()
    url_map.from_dict(validation_api(data))
    save_in_db(db, url_map)
    return jsonify(url_map.to_dict()), HTTPStatus.CREATED
