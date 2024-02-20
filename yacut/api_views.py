import re
from http import HTTPStatus

from flask import jsonify, request

from . import app, db
from .error_handlers import InvalidAPIUsage
from .models import URLMap
from .utils import get_short_url


@app.route('/api/id/<string:short>/', methods=['GET'])
def get_original_url(short):
    short_url = URLMap.query.filter_by(short=short).first()
    if not short_url:
        raise InvalidAPIUsage('Указанный id не найден', 404)
    return jsonify({"url": short_url.original}), HTTPStatus.OK


@app.route('/api/id/', methods=['POST'])
def create_short_url():
    data = request.get_json()
    if not data:
        raise InvalidAPIUsage('Отсутствует тело запроса')
    if 'url' not in data:
        raise InvalidAPIUsage('\"url\" является обязательным полем!')
    if not data.get('custom_id'):
        data['custom_id'] = get_short_url()
    elif URLMap.query.filter_by(short=data['custom_id']).first():
        raise InvalidAPIUsage('Предложенный вариант короткой ссылки уже существует.')
    elif not re.match(r'^[A-Za-z0-9_]{1,16}$', data['custom_id']):
        raise InvalidAPIUsage('Указано недопустимое имя для короткой ссылки')
    url_map = URLMap()
    url_map.from_dict(data)
    db.session.add(url_map)
    db.session.commit()
    return jsonify(url_map.to_dict()), HTTPStatus.CREATED
