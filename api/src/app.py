from flask import Flask, jsonify, make_response, send_file
from api.src.snowpark import snowpark
from api.src.postgres import postgres

app = Flask(__name__)
app.register_blueprint(snowpark, url_prefix='/snowpark')
app.register_blueprint(postgres, url_prefix='/postgres')


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
