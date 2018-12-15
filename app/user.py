from flask import Blueprint, jsonify

from sqlalchemy.orm.exc import NoResultFound

from app.database import User, Question
from . import get_logger


log = get_logger()


bp = Blueprint('user', __name__,
               static_folder='static',
               template_folder='templates')


@bp.route('/<int:user_id>', methods=['GET'])
def get_user(user_id):
    try:
        user = User.query.get(user_id)
    except NoResultFound as e:
        log.error(e)
        return jsonify({
            'status': 200,
            'code': 1,
            'msg': 'no user found'
        })
    return jsonify({
        'status': 200,
        'code': 0,
        'msg': 'get user info success',
        'user': {
            'id': user.id,
            'avatar': user.avatar,
            'nickname': user.nickname,
            'self_intro': user.self_intro
        }
    })


@bp.route('/<int:user_id>/<int:following_user_id>', methods=['PUT'])
def follow_user(user_id, following_user_id):
    try:
        user = User.query.get(user_id)
        following_user = User.query.get(following_user_id)
    except NoResultFound as e:
        log.error(e)
        return jsonify({
            'status': 200,
            'code': 1,
            'msg': 'no user found'
        })

    user.follow(following_user)

    return jsonify({
        'status': 200,
        'code': 0,
        'msg': 'following success'
    })


@bp.route('/<int:user_id>/followings', methods=['GET'])
def get_followings(user_id):
    try:
        user = User.query.get(user_id)
    except NoResultFound as e:
        log.error(e)
        return jsonify({
            'status': 200,
            'code': 1,
            'msg': 'no user found'
        })

    return jsonify({
        'status': 200,
        'code': 0,
        'msg': 'get success',
        'data': user.followings.all()
    })


@bp.route('/<int:user_id>/<int:question_id>', methods=['GET'])
def follow_question(user_id, question_id):
    try:
        user = User.query.get(user_id)
    except NoResultFound as e:
        log.error(e)
        return jsonify({
            'status': 200,
            'code': 1,
            'msg': 'no user found'
        })

    try:
        question = Question.query.get(question_id)
    except NoResultFound as e:
        log.error(e)
        return jsonify({
            'status': 200,
            'code': 1,
            'msg': 'no question found'
        })

    user.follow_question(question)

    return jsonify({
        'status': 200,
        'code': 0,
        'msg': 'follow question success'
    })


@bp.route('/<int:user_id>/questions', methods=['GET'])
def get_questions(user_id):
    try:
        user = User.query.get(user_id)
    except NoResultFound as e:
        log.error(e)
        return jsonify({
            'status': 200,
            'code': 1,
            'msg': 'no user found'
        })

    return jsonify({
        'status': 200,
        'code': 0,
        'msg': 'get success',
        'data': user.questions.all()
    })


@bp.route('/<int:user_id>/answers', methods=['GET'])
def get_answers(user_id):
    try:
        user = User.query.get(user_id)
    except NoResultFound as e:
        log.error(e)
        return jsonify({
            'status': 200,
            'code': 1,
            'msg': 'no user found'
        })

    return jsonify({
        'status': 200,
        'code': 0,
        'msg': 'get success',
        'data': user.answers.all()
    })


@bp.route('/<int:user_id>/comments', methods=['GET'])
def get_comments(user_id):
    try:
        user = User.query.get(user_id)
    except NoResultFound as e:
        log.error(e)
        return jsonify({
            'status': 200,
            'code': 1,
            'msg': 'no user found'
        })
    return jsonify({
        'status': 200,
        'code': 0,
        'msg': 'get success',
        'data': user.comments.all()
    })


@bp.route('/<int:user_id>/following_questions', methods=['GET'])
def get_following_questions(user_id):
    try:
        user = User.query.get(user_id)
    except NoResultFound as e:
        log.error(e)
        return jsonify({
            'status': 200,
            'code': 1,
            'msg': 'no user found'
        })

    return jsonify({
        'status': 200,
        'code': 0,
        'msg': 'get success',
        'data': user.following_questions.all()
    })
