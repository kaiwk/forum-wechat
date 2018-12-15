from flask import Blueprint, jsonify, request

from sqlalchemy.orm.exc import NoResultFound

from app.database import Question
from . import get_logger


log = get_logger()


bp = Blueprint('question', __name__,
               static_folder='static',
               template_folder='templates')


@bp.route('/<int:question_id>', methods=['GET'])
def get_question(question_id):
    try:
        question = Question.query.get(question_id)
    except NoResultFound as e:
        log.error(e)
        return jsonify({
            'status': 200,
            'code': 1,
            'msg': 'no question found'
        })

    return jsonify({
        'status': 200,
        'code': 0,
        'msg': 'get success',
        'question': {
            'id': question.id,
            'owner_id': question.user_id,
            'title': question.title,
            'content': question.content,
            'closed': question.closed
        }
    })


@bp.route('/', methods=['POST'])
def create_question():
    user_id = request.json['user_id']
    title = request.json['title']
    content = request.json['content']

    question = Question.save(title, content, user_id)

    return jsonify({
        'status': 200,
        'code': 0,
        'msg': 'question created',
        'question': {
            'id': question.id,
            'title': question.title,
            'content': question.content,
            'closed': question.closed
        }
    })


@bp.route('/<int:question_id>', methods=['PUT'])
def update_question(question_id):
    title = request.json['title']
    content = request.json['content']
    closed = request.json['closed']

    try:
        question = Question.query.get(question_id)
    except NoResultFound as e:
        log.error(e)
        return jsonify({
            'status': 200,
            'code': 1,
            'msg': 'no question found'
        })

    question.update(title, content, closed)

    return jsonify({
        'status': 200,
        'code': 0,
        'msg': 'question updated'
    })


@bp.route('/<int:question_id>/answers', methods=['GET'])
def get_answers(question_id):
    try:
        question = Question.query.get(question_id)
    except NoResultFound as e:
        log.error(e)
        return jsonify({
            'status': 200,
            'code': 1,
            'msg': 'no question found'
        })
    return jsonify({
        'status': 200,
        'code': 0,
        'msg': 'get success',
        'data': question.answers.all()
    })


@bp.route('/', methods=['GET'])
def search_question():
    fuzzy_match = request.json['fuzzy_match']
    pass
