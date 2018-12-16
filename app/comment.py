from flask import Blueprint, jsonify, request

from sqlalchemy.orm.exc import NoResultFound

from app.database import Comment
from . import get_logger


log = get_logger()


bp = Blueprint('comment', __name__)


@bp.route('/', methods=['POST'])
def create_comment():
    user_id = request.json['user_id']
    answer_id = request.json['answer_id']
    content = request.json['content']

    comment = Comment.save(content, user_id, answer_id)

    return jsonify({
        'status': 201,
        'code': 0,
        'msg': 'comment created',
        'comment': {
            'id': comment.id,
            'content': comment.content
        }
    })


@bp.route('/<int:comment_id>', methods=['GET'])
def get_comment(comment_id):
    try:
        comment = Comment.query.get(comment_id)
    except NoResultFound as e:
        log.error(e)
        return jsonify({
            'status': 404,
            'code': 1,
            'msg': 'no comment found'
        })

    return jsonify({
        'status': 200,
        'code': 0,
        'msg': 'get success',
        'comment': {
            'id': comment.id,
            'user_id': comment.user_id,
            'answer_id': comment.answer_id,
            'content': comment.content
        }
    })
