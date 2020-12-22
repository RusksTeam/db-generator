from flask import Flask, render_template, redirect, url_for, flash
from flask_restful import Api
from flask_jwt_extended import JWTManager
from api.resources.drybread import DryBread, DryBreadList
from api.models.drybread import DryBreadModel
from api.resources.user import User, UserList, UserLogin
from api.models.user import UserModel
import os


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'huuuuubert'
app.config['SECRET_KEY'] = 'top gun secret key'

api = Api(app)
api.add_resource(DryBread, '/api/drybread/<int:_id>')
api.add_resource(DryBreadList, '/api/drybreads')
api.add_resource(User, '/api/user/<int:id>')
api.add_resource(UserList, '/api/users')
api.add_resource(UserLogin, '/api/login')

jwt = JWTManager(app)

@jwt.user_claims_loader
def add_claims_to_jwt(identity):
    user = UserModel.find_by_id(identity)
    return {'is_admin': user.role == UserModel.ROLE_ADMIN}

@app.before_first_request
def initialize():
    db.create_all()
    from fill_tables import load_tables
    load_tables()
    global daily_drybread
    daily_drybread = DryBreadModel.get_random_drybread().json()

@app.route('/')
def index():
    return render_template('index.html', question=daily_drybread['question'], answer=daily_drybread['answer'])

@app.route('/update_daily_drybread')
def update_daily_drybread():
    global daily_drybread
    daily_drybread = DryBreadModel.get_random_drybread().json()
    flash('Drybread has been successfully updated.')
    return redirect(url_for('index'))

if __name__ == "__main__":
    from db import db
    db.init_app(app)
    app.run('0.0.0.0', debug=True)