import sys
import urllib
from flask import Flask, jsonify
from flask import request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
imageName = ""
personName = ""


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/name', methods=['GET'])
def name():
    message = {'name': personName}
    return jsonify(message)


@app.route('/images', methods=['POST'])
def image():
    if request.method == 'POST':
        global imageName, personName
        imageName = request.get_json()["name"]
        personName = request.get_json()["id"]
        print(request.get_json(), file=sys.stderr)
        if request.get_json().get("content"):
            response = urllib.request.urlopen(request.get_json()["content"])
            with open(request.get_json()["name"], 'wb') as f:
                f.write(response.file.read())
        return {'success': True}, 200


@app.route('/questions', methods=['POST'])
def questions():
    if request.method == 'POST':
        global personName
        json = request.get_json()
        json['imageName'] = imageName
        json['personName'] = personName
        personName = ""
        print(json, file=sys.stderr)
        with open("dotaznik.txt", "a", encoding="utf-8") as f:
            f.write(str(request.get_json()) + "\n")
        return {'success': True}, 200


# @app.route('/startingQuestions', methods=['POST'])
# def startingQuestions():
#     if request.method == 'POST':
#         json = request.get_json()
#         print(json, file=sys.stderr)
#         with open("dotaznik.txt", "a") as f:
#             f.write(str(request.get_json()) + "\n")
#         return {'success': True}, 200


@app.route('/positions', methods=['POST'])
def positions():
    if request.method == 'POST':
        global personName
        print(request.get_json(), file=sys.stderr)
        personName = request.get_json()["id"]
        with open(request.get_json()['imageName'][:-4] + ".txt", "a", encoding="utf-8") as f:
            f.write(str(request.get_json()) + "\n")
        return {'success': True}, 200


if __name__ == '__main__':
    app.run()

