from flask import Blueprint


bp = Blueprint('main', __name__,
               static_folder='static',
               template_folder='templates')


@bp.route('/')
def hello():
    return 'hello, world'
