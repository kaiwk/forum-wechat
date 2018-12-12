import requests

from flask import Blueprint, request, jsonify, current_app

from . import get_logger

bp = Blueprint('wx_auth', __name__,
               static_folder='static',
               template_folder='templates')


WECHAT_SECRET_KEY = 'd50802e34c18bc1b6dea48894291cef7'
WECHAT_APP_ID = 'wx91904b5fa3e40744'
API_CODE2SESSION = 'https://api.weixin.qq.com/sns/jscode2session?appid={appid}&secret={secret}&js_code={jscode}&grant_type=authorization_code'


log = get_logger()


@bp.route('/')
def wx_auth():
    code = request.json['code']
    log.debug('code: %s', code)
    wx_auth_url = API_CODE2SESSION.format(appid=WECHAT_APP_ID,
                                          secret=WECHAT_SECRET_KEY, jscode=code)
    res = requests.get(wx_auth_url).content
    log.debug(res)
    return res
