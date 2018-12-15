from flask import Blueprint, jsonify, request

from sqlalchemy.orm.exc import NoResultFound

from app.database import Answer
from . import get_logger


log = get_logger()


bp = Blueprint('answer', __name__)


@bp.route('/<int:answer_id>', methods=['GET'])
def get_answer(answer_id):
    try:
        answer = Answer.query.get(answer_id)
    except NoResultFound as e:
        log.error(e)
        return jsonify({
            'status': 200,
            'code': 1,
            'msg': 'no answer found'
        })

    return jsonify({
        'status': 200,
        'code': 0,
        'msg': 'get success',
        'answer': {
            'id': answer.id,
            'user_id': answer.user_id,
            'question_id': answer.question_id,
            'content': answer.content,
            'anonymous': answer.anonymous
        }
    })


@bp.route('/<int:answer_id>/comments', methods=['GET'])
def get_comments(answer_id):
    try:
        answer = Answer.query.get(answer_id)
    except NoResultFound as e:
        log.error(e)
        return jsonify({
            'status': 200,
            'code': 1,
            'msg': 'no answer found'
        })

    return jsonify({
        'status': 200,
        'code': 0,
        'msg': "get success",
        'data': answer.comments.all()
    })


@bp.route('/', methods=['POST'])
def create_answer():
    user_id = request.json['user_id']
    question_id = request.json['question_id']
    anonymous = request.json['anonymous']
    content = request.json['content']

    answer = Answer.save(content, anonymous, user_id, question_id)

    return jsonify({
        'status': 200,
        'code': 0,
        'msg': 'answer created',
        'answer': {
            'id': answer.id,
            'content': answer.content,
            'anonymous': answer.anonymous
        }
    })
