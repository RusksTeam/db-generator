import random
from db import db

class DryBreadModel(db.Model):
    __tablename__ = 'drybreads'

    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(200))
    answer = db.Column(db.String(200))

    def __init__(self, question, answer):
        self.question = question
        self.answer = answer

    def json(self):
        return {'id': self.id, 'question': self.question, 'answer': self.answer}

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

    @classmethod
    def find_all(cls):
        return cls.query.all()

    @classmethod
    def get_random_drybread(cls):
        return cls.query.offset(int(cls.query.count() * random.random())).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
