from flask import Flask, request, jsonify
from json2xml import json2xml
from json2xml.utils import readfromstring
import json

app = Flask(__name__)


@app.route('/projects')
def projects():
    todo_response = [
        {
            'id': 1,
            'name': "Project 1",
            'type': "activity",
            'due': "2016-02-11T09:46:56.023Z",
            'tasks': [
                {
                    'done': True,
                    'id': 1,
                    'name': "Task 1",
                },
                {
                    'done': True,
                    'id': 2,
                    'name': "Task 2",
                },
                {
                    'done': True,
                    'id': 3,
                    'name': "Task 3",
                },
                {
                    'done': True,
                    'id': 4,
                    'name': "Task 4",
                },
            ]
        }
    ]
    if request.headers['accept'] == 'application/xml':
        return json2xml.Json2xml(readfromstring(json.dumps(todo_response)), wrapper = 'projects').to_xml()
    else:
        return jsonify(todo_response)

if __name__ == '__main__':
    app.run(debug=True, port=5001)