import sys
import urllib
from flask import Flask
from flask import request
from flask_cors import CORS


class Person:
    def __init__(self, pName, pImageName):
        self.name = pName
        self.imageName = pImageName


app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})
persons = []


@app.route('/')
def start():
    return 'Server is up and running'


@app.route('/images', methods=['POST'])
def image():
    if request.method == 'POST':
        json = request.get_json()
        for person in persons:
            if person.name == json["id"]:
                person.imageName = json["name"]

        print(request.get_json(), file=sys.stderr)
        if request.get_json().get("content"):
            response = urllib.request.urlopen(request.get_json()["content"])
            with open("data/" + request.get_json()["name"], 'wb') as f:
                f.write(response.file.read())
        return {'success': True}, 200


@app.route('/questions', methods=['POST'])
def questions():
    if request.method == 'POST':
        json = request.get_json()
        if 'age' in json:
            persons.append(Person(json['name'], ''))

        elif 'answers' in json:
            removable_person = None
            for person in persons:
                if person.name == json['name']:
                    removable_person = person
            persons.remove(removable_person)

        else:
            for person in persons:
                if person.name == json['name']:
                    json['imageName'] = person.imageName
        print(json, file=sys.stderr)
        with open("data/dotaznik.txt", "a", encoding="utf-8") as f:
            f.write(str(request.get_json()) + "\n")
        return {'success': True}, 200


@app.route('/positions', methods=['POST'])
def positions():
    if request.method == 'POST':
        print(request.get_json(), file=sys.stderr)
        with open("data/" + request.get_json()['imageName'][:-4] + ".txt", "a",
                  encoding="utf-8") as f:
            f.write(str(request.get_json()) + "\n")
        return {'success': True}, 200


if __name__ == '__main__':
    app.run()
