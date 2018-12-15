import time

import requests
import jwt

from flask import Blueprint, request, jsonify, current_app
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound

from app.database import User
from . import get_logger


bp = Blueprint('wx_auth', __name__)


API_CODE2SESSION = 'https://api.weixin.qq.com/sns/jscode2session?appid={appid}&secret={secret}&js_code={jscode}&grant_type=authorization_code'


log = get_logger()


@bp.route('/')
def wechat_auth():
    auth_code = request.json['auth_code']
    avatar = request.json['avatar']
    nickname = request.json['nickname']

    log.debug('auth_code: %s', auth_code)
    wx_auth_url = API_CODE2SESSION.format(appid=current_app.config['WECHAT_APP_ID'],
                                          secret=current_app.config['WECHAT_SECRET_KEY'],
                                          jscode=auth_code)
    res = requests.get(wx_auth_url).json()
    open_id = res['open_id']

    try:
        user = User.query.filter_by(open_id=open_id).one()
        log.info('User<%s> already exists', open_id)
    except NoResultFound:
        log.info('User<%s> not exists, now save it', open_id)
        user = User.save(open_id, avatar, nickname)
        return jsonify({'status': 200, 'code': 0, 'msg': 'User has been saved', 'user_id': user.id})
    except MultipleResultsFound:
        return jsonify({'status': 200, 'code': 2, 'msg': 'User has been saved multiple times'})

    return jsonify({'status': 200, 'code': 1, 'msg': 'User already exists', 'user_id': user.id})


def create_token(open_id):
    payload = {
        'iss': 'iss',
        'iat': int(time.time()),
        'exp': int(time.time()) + 86400 * 7,
        'sub': open_id
    }
    token = jwt.encode(payload, current_app.config['JWT_SECRET_KEY'], algorithm='HS256')
    return token


def get_open_id(token):
    jwt.decode(token, current_app.config['JWT_SECRET_KEY'], algorithms='HS256')
