import datetime

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from sqlalchemy import Column, Boolean, DateTime, Integer, Text

db = SQLAlchemy()
migrate = Migrate()

class Test(db.Model):
    __tablename__ = 'tasks'
    id = Column(Integer, primary_key=True)
    body = Column(Text, nullable=False)
    selected = Column(Boolean, default=False)
    updated_at = Column(DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.utcnow)

    def __repr__(self):
        return '<Test {}, finished:{}>'.format(self.id, self.selected)


def init_app(app):
    db.init_app(app)
    migrate.init_app(app, db)
