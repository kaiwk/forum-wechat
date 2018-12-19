from flask import Blueprint, jsonify, request

from sqlalchemy import func
from sqlalchemy.orm.exc import NoResultFound

from app.database import User, Answer, Question
from . import get_logger


log = get_logger()


bp = Blueprint('page', __name__)


@bp.route('/following_questions_update/user/<int:user_id>', methods=['GET'])
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
            u = User.query.get(a.user_id)
            d['question_title'] = a.question.title
            d['nickname'] = u.nickname
            d['avatar'] = u.avatar
            d['answer_count'] = a.question.answers.count()
            data_list.append(d)

    return jsonify({
        'status': 200,
        'code': 0,
        'msg': 'get success',
        'data': data_list
    })


@bp.route('/comment_list/', methods=['GET'])
def get_comments():

    answer_id = request.args.get('answer_id')

    try:
        answer = Answer.query.get(answer_id)
    except NoResultFound as e:
        log.error(e)
        return jsonify({
            'status': 404,
            'code': 1,
            'msg': 'no answer found'
        })

    data_list = []

    for a in answer.comments.all():
        d = a.as_dict()
        u = User.query.get(a.user_id)
        d['nickname'] = u.nickname
        d['avatar'] = u.avatar
        data_list.append(d)

    return jsonify({
        'status': 200,
        'code': 0,
        'msg': "get success",
        'data': data_list
    })


@bp.route('/index/', methods=['GET'])
def index():
    questions = Question.query.order_by(func.rand()).all()

    data_list = []
    for q in questions:
        answer = q.answers.first()
        if answer:
            d = q.as_dict()
            u = User.query.get(answer.user_id)
            d['answer_id'] = answer.id
            d['answer_content'] = answer.content
            d['answer_user_id'] = answer.user_id
            d['nickname'] = u.nickname
            d['avatar'] = u.avatar
            data_list.append(d)

    return jsonify({
        'status': 200,
        'code': 0,
        'msg': 'get success',
        'data': data_list
    })
