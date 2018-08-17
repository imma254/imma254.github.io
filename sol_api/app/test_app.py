from copy import deepcopy
import unittest
import json

import app

BASE_URL = 'http://127.0.0.1:5000/api/v1/questions'
BAD_ITEM_URL = '{}/5'.format(BASE_URL)
GOOD_ITEM_URL = '{}/3'.format(BASE_URL)


class TestSolApi(unittest.TestCase):

    def setUp(self):
        self.backup_qstns = deepcopy(app.questions)
        self.backup_answers = deepcopy(app.answers)
        self.app = app.app.test_client()
        self.app.testing = True

    def test_get_all_questions(self):
        response = self.app.get(BASE_URL)
        data = json.loads(response.get_data())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(data['questions']), 3)

    def test_get_one_question(self):
        response = self.app.get(BASE_URL)
        data = json.loads(response.get_data())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['questions'][0]['title'], 'VBA MsgBox pop-up according to cell value')

    def test_qstn_not_exist(self):
        response = self.app.get(BAD_ITEM_URL)
        self.assertEqual(response.status_code, 404)

    def test_post_qstn(self):
        qstn = {"title": "some_qstn"}
        response = self.app.post(BASE_URL,
                                 data=json.dumps(qstn),
                                 content_type='application/json')
        self.assertEqual(response.status_code, 400)
        # votes field cannot take string
        qstn = {"title": "JAVA", "votes": 'string'}
        response = self.app.post(BASE_URL,
                                 data=json.dumps(qstn),
                                 content_type='application/json')
        self.assertEqual(response.status_code, 400)
        # validation: both fields are required, votes field takes int
        qstn = {"title": "JAVA", "votes": 20}
        response = self.app.post(BASE_URL,
                                 data=json.dumps(qstn),
                                 content_type='application/json')
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.get_data())
        self.assertEqual(data['qstn']['id'], 4)
        self.assertEqual(data['qstn']['title'], 'JAVA')
        # validation for duplicate entries
        qstn = {"title": "VBA MsgBox pop-up according to cell value", "votes": 10}
        response = self.app.post(BASE_URL,
                                 data=json.dumps(qstn),
                                 content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_post_answer(self):
        answer = {"desc": "the answer"}
        response = self.app.post(BASE_URL,
                                 data=json.dumps(answer),
                                 content_type='application/json')
        self.assertEqual(response.status_code, 400)
        # votes field cannot take string
        answer = {"desc": "the answer", "votes": 'string'}
        response = self.app.post(BASE_URL,
                                 data=json.dumps(answer),
                                 content_type='application/json')
        self.assertEqual(response.status_code, 400)


if __name__ == "__main__":
    unittest.main()
