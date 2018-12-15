from flask import Blueprint, jsonify

from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import IntegrityError

from app.database import User, Question, Answer
from . import get_logger


log = get_logger()


bp = Blueprint('user', __name__)


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


@bp.route('/<int:user_id>/user/<int:following_user_id>', methods=['PUT'])
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

    try:
        user.follow(following_user)
    except IntegrityError as e:
        log.error(e)
        return jsonify({
            'status': 200,
            'code': 2,
            'msg': 'user has been followed'
        })

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
        'data': [u.as_dict() for u in user.followings.all()]
    })


@bp.route('/<int:user_id>/question/<int:question_id>', methods=['PUT'])
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

    try:
        user.follow_question(question)
    except IntegrityError as e:
        log.error(e)
        return jsonify({
            'status': 200,
            'code': 2,
            'msg': 'question has been followed'
        })

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
        'data': [a.as_dict() for a in user.answers.all()]
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
        'data': [c.as_dict() for c in user.comments.all()]
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


@bp.route('/<int:user_id>/following_questions/answers', methods=['GET'])
def get_following_questions_answers(user_id):
    try:
        user = User.query.get(user_id)
    except NoResultFound as e:
        log.error(e)
        return jsonify({
            'status': 200,
            'code': 1,
            'msg': 'no user found'
        })

    flw_qst_ans = []
    answers = Answer.query.all()

    for a in answers:
        if a.question in user.following_questions:
            flw_qst_ans.append(a)

    return jsonify({
        'status': 200,
        'code': 0,
        'msg': 'get success',
        'data': [a.as_dict() for a in flw_qst_ans]
    })
