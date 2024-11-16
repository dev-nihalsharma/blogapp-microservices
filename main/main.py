from os import abort
from flask import Flask, jsonify
from dataclasses import dataclass
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import requests
from sqlalchemy import UniqueConstraint
from flask_migrate import Migrate

from producer import publish

app = Flask(__name__)

app.app_context().push()
app.config["SQLALCHEMY_DATABASE_URI"] = 'postgresql://postgres:postgres@db/postgres'

CORS(app)
db = SQLAlchemy(app)

migrate = Migrate(app, db)

@dataclass
class Blog(db.Model):
    id: int
    title: str
    content: str
    image: str

    id = db.Column(db.Integer, primary_key=True, autoincrement=False)
    title = db.Column(db.String(200))
    content = db.Column(db.String(2000))
    image = db.Column(db.String(200))


@dataclass
class BlogUser(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    product_id = db.Column(db.Integer)

    UniqueConstraint('user_id', 'product_id', name='user_product_unique')


@app.route('/api/blogs')
def index():
    return jsonify(Blog.query.all())

@app.route('/api/blogs/<int:id>/like', methods=['POST'])
def like(id):
    req = requests.get('http://docker.for.mac.localhost:8000/api/user')
    json = req.json()

    try:
        blogUser = BlogUser(user_id=json['id'], product_id=id)
        db.session.add(blogUser)
        db.session.commit()

        publish('blog_liked', {'id': id})
    except:
        abort(400, 'You already liked this blog')

    return jsonify({ 
        'message': 'success'
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')