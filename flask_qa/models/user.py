from flask_login import UserMixin
from werkzeug.security import generate_password_hash
from ..utils import db


class User(db.Model, UserMixin):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(50))
    password = db.Column(db.String(100))
    expert = db.Column(db.Boolean)
    admin = db.Column(db.Boolean)

    questions_asked = db.relationship(
        'Question', 
        foreign_keys = 'Question.asked_by_id', 
        backref = 'asker', 
        lazy = True
    )

    answers_requested = db.relationship(
        'Question',
        foreign_keys = 'Question.expert_id',
        backref = 'expert',
        lazy = True
    )

    @property
    def unhashed_password(self):
        raise AttributeError('Cannot view unhashed password!')

    @unhashed_password.setter
    def unhashed_password(self, unhashed_password):
        self.password = generate_password_hash(unhashed_password)


    def __repr__(self):
        return f"<User {self.id}>"

    def save(self):
        db.session.add(self)
        db.session.commit()
    
    @classmethod
    def get_by_id(cls, id):
        return cls.query.get_or_404(id)

    def delete(self):
        db.session.delete(self)
        db.session.commit()
