from ..utils import db

class Question(db.Model):
    __tablename__ = 'question'

    id = db.Column(db.Integer, primary_key = True)
    question = db.Column(db.Text)
    answer = db.Column(db.Text)
    asked_by_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    expert_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return f"<Question {self.id}>"

    def save(self):
        db.session.add(self)
        db.session.commit()
    
    @classmethod
    def get_by_id(cls, id):
        return cls.query.get_or_404(id)

    def delete(self):
        db.session.delete(self)
        db.session.commit()