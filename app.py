from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app =  Flask(__name__)
CORS(app)
app.secret_key = "anything ok"
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://postgres:123456@localhost:5432/type-racer'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)

class User(UserMixin, db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String)
    score_history = db.relationship("Score", backref="user", lazy=True)

class Score(db.Model):
    __tablename__ = 'score'
    id = db.Column(db.Integer, primary_key = True)
    time =  db.Column(db.Integer)
    wpm =  db.Column(db.Integer)
    errors =  db.Column(db.Integer)
    excerpt_id = db.Column(db.Integer, db.ForeignKey('excerpt.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    
class Excerpt(db.Model):
    __tablename__ = 'excerpt'
    id = db.Column(db.Integer, primary_key = True)
    body = db.Column(db.Text)
    score_history = db.relationship("Score", backref="excerpt", lazy=True)

db.create_all()

@app.route('/excerpts')
def root():
    return jsonify(
        ['a','b','c']
    )

@app.route('/scores', methods = ['GET','POST'])
def create_score():
    score = Score(
        user_id = 1, 
        time = request.get_json()['time'] , 
        wpm = request.get_json()['wpm'], 
        errors = request.get_json()['errorCount']
        )
    db.session.add(score)
    db.session.commit()
    res = {
        "user_id" : score.user_id,
        "time" : score.time,
        "wpm" : score.wpm,
        "errors" : score.errors
    }
    return jsonify(res)

if __name__ == "__main__":
  app.run(debug=True, ssl_context='adhoc')
