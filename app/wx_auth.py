import json
import requests
import jwt
import time

from flask import Blueprint, request, jsonify, current_app

from . import get_logger


bp = Blueprint('wx_auth', __name__,
               static_folder='static',
               template_folder='templates')


API_CODE2SESSION = 'https://api.weixin.qq.com/sns/jscode2session?appid={appid}&secret={secret}&js_code={jscode}&grant_type=authorization_code'


log = get_logger()


@bp.route('/')
def wx_auth():
    auth_code = request.args.get('auth_code')

    log.debug('auth_code: %s', auth_code)
    wx_auth_url = API_CODE2SESSION.format(appid=current_app.config['WECHAT_APP_ID'],
                                          secret=current_app.config['WECHAT_SECRET_KEY'], jscode=auth_code)
    res = requests.get(wx_auth_url).content.decode()
    res = json.loads(res)

    log.info(res)

    return jsonify(res)


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
