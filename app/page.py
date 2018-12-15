from flask import Blueprint, jsonify

from sqlalchemy.orm.exc import NoResultFound

from app.database import User, Answer
from . import get_logger


log = get_logger()


bp = Blueprint('page', __name__)


@bp.route('/following_questions_update/user/<int:user_id>/', methods=['GET'])
def following_questions_answers(user_id):
    try:
        user = User.query.get(user_id)
    except NoResultFound as e:
        log.error(e)
        return jsonify({
            'status': 404,
            'code': 1,
            'msg': 'no user found'
        })

    data_list = []
    answers = Answer.query.all()

    for a in answers:
        if a.question in user.following_questions:
            # add question data
            d = a.as_dict()
            d['question_title'] = a.question.title
            d['nickname'] = User.query.get(a.user_id).nickname
            d['answer_count'] = a.question.answers.count()
            data_list.append(d)

    return jsonify({
        'status': 200,
        'code': 0,
        'msg': 'get success',
        'data': data_list
    })
