from flask import Flask, jsonify, abort, make_response, request

NOT_FOUND = 'DATA Not found'
BAD_REQUEST = 'Bad request'

app = Flask(__name__)

questions = [
    {
        'id': 1,
        'title': 'VBA MsgBox pop-up according to cell value',
        'votes': 10
    },
    {
        'id': 2,
        'title': 'Method order resolving in multiple and multilevel inheritance in python while calling the constructor.',
        'votes': 300,
    },
    {
        'id': 3,
        'title': 'organizing android + firebase project for dev staging production',
        'votes': 20,
    },
]

answers = [
    {
        'id': 1,
        'desc': 'VBA MsgBox pop-up according to cell value',
        'votes': 10
    },
    {
        'id': 2,
        'desc': 'manu',
        'votes': 10
    }
]


def _get_qstn(id):
    return [qstn for qstn in questions if qstn['id'] == id]


def _entry_exists_for_qstn(title):
    return [qstn for qstn in questions if qstn["title"] == title]


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': NOT_FOUND}), 404)


@app.errorhandler(400)
def bad_request(error):
    return make_response(jsonify({'error': BAD_REQUEST}), 400)


@app.route('/api/v1/questions', methods=['GET'])
def get_all_questions():
    return jsonify({'questions': questions})


@app.route('/api/v1/questions/<int:id>/answers', methods=['GET'])
def get_all_answers(id):
    qstn = _get_qstn(id)
    if not qstn:
        abort(404)
    return jsonify({'answers': answers})


@app.route('/api/v1/questions/<int:id>', methods=['GET'])
def get_one_question(id):
    qstn = _get_qstn(id)
    if not qstn:
        abort(404)
    return jsonify({'questions': qstn})


@app.route('/api/v1/questions', methods=['POST'])
def post_qstn():
    if not request.json or 'title' not in request.json:
        abort(400)
    qstn_id = questions[-1].get("id") + 1
    title = request.json.get('title')
    if _entry_exists_for_qstn(title):
        abort(400)
    votes = request.json.get('votes')
    if type(votes) is not int:
        abort(400)
    qstn = {"id": qstn_id, "title": title, "votes": votes}
    questions.append(qstn)
    return jsonify({'qstn': qstn}), 201


@app.route('/api/v1/questions/<int:id>', methods=['POST'])
def post_answer(id):
    if not request.json or 'desc' not in request.json:
        abort(400)
    answer_id = answers[-1].get("id") + 1
    desc = request.json.get('desc')
    votes = request.json.get('votes')
    if type(votes) is not int:
        abort(400)
    answer = {"id": answer_id, "desc": desc, "votes": votes}
    answers.append(answer)
    return jsonify({'answer': answer}), 201


if __name__ == '__main__':
    app.run(debug=True)
