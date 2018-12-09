from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()

followings = db.Table('followings',
                      db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
                      db.Column('following_id', db.Integer, db.ForeignKey('user.id'), primary_key=True))

following_questions = db.Table('following_questions',
                               db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
                               db.Column('question_id', db.Integer, db.ForeignKey('question.id'), primary_key=True))


class CreateUpdateTimeMixin:
    created_on = db.Column(db.DateTime, server_default=db.func.now())
    updated_on = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())


class User(db.Model, CreateUpdateTimeMixin):
    id = db.Column(db.Integer, primary_key=True)
    open_id = db.Column(db.String(64))
    questions = db.relationship('Question', backref='owner')
    comments = db.relationship('Comment', backref='owner')
    answers = db.relationship('Answer', backref='owner')
    followings = db.relationship('User', secondary=followings,
                                 primaryjoin=lambda: User.id == followings.c.user_id,
                                 secondaryjoin=lambda: User.id == followings.c.following_id,
                                 backref='followers')
    following_questions = db.relationship('Question', secondary=following_questions, backref='followers')

    def __repr__(self):
        return '<User:{}, openid:{}>'.format(self.id, self.open_id)


class Comment(db.Model, CreateUpdateTimeMixin):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    answer_id = db.Column(db.Integer, db.ForeignKey('answer.id'), nullable=False)

    def __repr__(self):
        return '<Comment:{}>'.format(self.id)


class Answer(db.Model, CreateUpdateTimeMixin):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'), nullable=False)
    comments = db.relationship('Comment', backref='answer')

    def __repr__(self):
        return '<Answer:{}>'.format(self.id)


class Question(db.Model, CreateUpdateTimeMixin):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    answers = db.relationship('Answer', backref='question')

    def __repr__(self):
        return '<Question:{}>'.format(self.id)


def init_app(app):
    db.init_app(app)
    migrate.init_app(app, db)
