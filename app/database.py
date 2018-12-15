import datetime

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()

followings = db.Table('followings',
                      db.Column('user_id', db.Integer,
                                db.ForeignKey('user.id'), primary_key=True),
                      db.Column('following_id', db.Integer,
                                db.ForeignKey('user.id'), primary_key=True))

following_questions = db.Table('following_questions',
                               db.Column('user_id', db.Integer,
                                         db.ForeignKey('user.id'), primary_key=True),
                               db.Column('question_id', db.Integer,
                                         db.ForeignKey('question.id'), primary_key=True))


class CreateUpdateTimeMixin:
    created_on = db.Column(db.DateTime, server_default=db.func.now())
    updated_on = db.Column(db.DateTime, server_default=db.func.now(),
                           server_onupdate=db.func.now())


class DictSerializable:
    def as_dict(self):
        result = dict()
        for key in self.__mapper__.c.keys():
            val = getattr(self, key)
            if type(val) == datetime.datetime:
                val = str(val)
            result[key] = val
        return result


class User(db.Model, CreateUpdateTimeMixin, DictSerializable):
    id = db.Column(db.Integer, primary_key=True)
    open_id = db.Column(db.String(128), nullable=False)
    avatar = db.Column(db.String(200))
    nickname = db.Column(db.String(30))
    self_intro = db.Column(db.String(200))
    questions = db.relationship('Question', backref='owner', lazy='dynamic')
    comments = db.relationship('Comment', backref='owner', lazy='dynamic')
    answers = db.relationship('Answer', backref='owner', lazy='dynamic')
    followings = db.relationship('User', secondary=followings,
                                 primaryjoin=(id == followings.c.user_id),
                                 secondaryjoin=(id == followings.c.following_id),
                                 backref=db.backref('followers', lazy='dynamic'), lazy='dynamic')
    following_questions = db.relationship('Question', secondary=following_questions,
                                          backref=db.backref('followers', lazy='dynamic'),
                                          lazy='dynamic')

    def __init__(self, open_id, avatar, nickname):
        self.open_id = open_id
        self.avatar = avatar
        self.nickname = nickname

    def __repr__(self):
        return '<User:{}, openid:{}>'.format(self.id, self.open_id)

    @staticmethod
    def save(open_id, avatar, nickname):
        user = User(open_id, avatar, nickname)
        db.session.add(user)
        db.session.commit()
        return user

    def follow(self, user):
        self.followings.append(user)
        db.session.commit()

    def unfollow(self, user):
        self.followings.remove(user)
        db.session.commit()

    def follow_question(self, question):
        self.following_questions.append(question)
        db.session.commit()

    def unfollow_question(self, question):
        self.following_questions.remove(question)
        db.session.commit()


class Comment(db.Model, CreateUpdateTimeMixin, DictSerializable):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    answer_id = db.Column(db.Integer, db.ForeignKey('answer.id'), nullable=False)

    def __repr__(self):
        return '<Comment:{}>'.format(self.id)

    def __init__(self, content, user_id, answser_id):
        self.content = content
        self.user_id = user_id
        self.answer_id = answser_id

    @staticmethod
    def save(content, user_id, answser_id):
        comment = Comment(content, user_id, answser_id)
        db.session.add(comment)
        db.session.commit()
        return comment

    @staticmethod
    def remove(comment_id):
        comment = Comment.query.get(comment_id)
        db.session.delete(comment)
        db.session.commit()

    @staticmethod
    def update(comment_id, content):
        comment = Comment.query.get(comment_id)
        comment.content = content
        db.session.commit()


class Answer(db.Model, CreateUpdateTimeMixin, DictSerializable):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    anonymous = db.Column(db.Boolean, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'), nullable=False)
    comments = db.relationship('Comment', backref='answer', lazy='dynamic')

    def __init__(self, content, anonymous, user_id, question_id):
        self.content = content
        self.anonymous = anonymous
        self.user_id = user_id
        self.question_id = question_id

    def __repr__(self):
        return '<Answer:{}>'.format(self.id)

    @staticmethod
    def save(content, anonymous, user_id, question_id):
        answer = Answer(content, anonymous, user_id, question_id)
        db.session.add(answer)
        db.session.commit()
        return answer

    @staticmethod
    def remove(answer_id):
        answer = Answer.query.get(answer_id)
        db.session.delete(answer)
        db.session.commit()

    @staticmethod
    def update(answer_id, content):
        answer = Answer.query.get(answer_id)
        answer.content = content
        db.session.commit()

    def add_comment(self, comment):
        self.comments.append(comment)
        db.session.commit()


class Question(db.Model, CreateUpdateTimeMixin, DictSerializable):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(140), nullable=False)
    content = db.Column(db.Text, nullable=False)
    closed = db.Column(db.Boolean, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    answers = db.relationship('Answer', backref='question', lazy='dynamic')

    def __init__(self, title, content, user_id):
        self.title = title
        self.content = content
        self.user_id = user_id

    def __repr__(self):
        return '<Question:{}>'.format(self.id)

    @staticmethod
    def save(title, content, user_id):
        question = Question(title, content, user_id)
        db.session.add(question)
        db.session.commit()
        return question

    @staticmethod
    def remove(question_id):
        question = Question.query.get(question_id)
        db.session.delete(question)
        db.session.commit()

    def update(self, title=None, content=None, closed=None):
        if title:
            self.title = title
        if content:
            self.content = content
        if closed:
            self.closed = closed
        db.session.commit()

    def add_answer(self, answer):
        self.answers.append(answer)
        db.session.commit()


def init_app(app):
    db.init_app(app)
    migrate.init_app(app, db)
