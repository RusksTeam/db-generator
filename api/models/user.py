from db import db
from hashlib import sha512


class UserModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30))
    password = db.Column(db.String(250))
    role = db.Column(db.Integer)
    (ROLE_ADMIN, ROLE_MODERATOR, ROLE_USER) = (0, 1, 2)

    def __init__(self, username, password, role=2):
        self.username = username
        password_hashed = sha512(password.encode('utf-8')).hexdigest()
        self.password = password_hashed
        self.role = role

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    def json(self):
        return {'id': self.id, 'username': self.username, 'role': self.role}

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

    @classmethod
    def find_all(cls):
        return cls.query.all()

