from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)

    def __init__(self, username, email):
        self.username = username
        self.email = email

    def __repr__(self):
        return '<User %r>' % self.username

    def to_json(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email
        }

@app.route('/')
def hello_world():
    return 'Hello, world'

@app.route('/users/')
def users_list():
    users = User.query.all()
    return jsonify([u.to_json() for u in users])

@app.route('/users/<int:user_id>/')
def user_detail(user_id):
    user = User.query.filter_by(id=user_id).first_or_404()
    return jsonify(user.to_json())
