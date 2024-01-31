from flask import Flask, jsonify, make_response, send_file
from api.src.postgres import postgres
from urllib.parse import quote_plus
from api.src.config import postgres_creds
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = (
    postgres_creds['sql_dialect'] + "+" + postgres_creds['adapter'] + "://" +
    quote_plus(postgres_creds['username']) + ":" +
    quote_plus(postgres_creds['password']) + "@" +
    postgres_creds['host'] + ":" +
    str(postgres_creds['port']) + "/" +
    postgres_creds['database']
)
db.init_app(app)
app.register_blueprint(postgres, url_prefix='/postgres')


class Passengers(db.Model):
    __table_name__ = 'passengers'

    passengerid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    survived = db.Column(db.Integer, nullable=False)
    pclass = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String(), nullable=False)
    sex = db.Column(db.String(), nullable=False)
    age = db.Column(db.Float(), nullable=True)
    sibsp = db.Column(db.Integer, nullable=False)
    parch = db.Column(db.Integer, nullable=False)
    ticket = db.Column(db.String(), nullable=False)
    fare = db.Column(db.Float(), nullable=True)
    cabin = db.Column(db.String(), nullable=True)
    embarked = db.Column(db.String(), nullable=False)


with app.app_context():
    db.create_all()


@app.route("/")
def default():
    return make_response(jsonify(result='Nothing to see here'))


@app.route("/test")
def tester():
    return send_file("api_test.html")


@app.errorhandler(404)
def resource_not_found(e):
    return make_response(jsonify(error='Not found!'), 404)


if __name__ == '__main__':
    app.run(port=8001, host='127.0.0.1')
