import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category




class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""
    cur_question_id = None
    question_str = "dummy question"
    
    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgresql://triuser:tripass@{}/{}".format('localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    Done
    Write at least one test for each test for successful operation and for expected errors.
    """
    def test_get_questions(self):
        # print("****** runtest test_get_questions")
        """Tests question pagination success"""

        # get response and load data
        response = self.client().get('/questions')
        data = json.loads(response.data)

        # check status code and message
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)

        # ---- check if the pagination is working correctly or not
        
        # maximum question in one page is 10
        if data['total_questions'] > 10:
            self.assertTrue(len(data['questions'])<=10)
    
    def test_get_questions_with_category(self):

        category_id = 1
        # get response and load data
        response = self.client().get(f'/questions?category_id={category_id}')
        data = json.loads(response.data)
        # check status code and message
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        if response.status_code == 200:
            for question in data['questions']:
                self.assertEqual(question['category'],category_id)

        

        # ---- check if the pagination is working correctly or not
        
        # maximum question in one page is 10
        if data['total_questions'] > 10:
            self.assertTrue(len(data['questions'])<=10)

    def test_get_catagories(self):
        # print("****** runtest test_get_questions")
        """Tests question pagination success"""

        # get response and load data
        response = self.client().get('/categories')
        data = json.loads(response.data)

        # check status code and message
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_get_2nd_page_questions(self):
        # print("****** runtest test_get_2nd_page_questions")
        """Tests page param to see if it acutually get a different page of question or not"""
         
        # first get the first page
        response = self.client().get('/questions')
        data = json.loads(response.data)
         # check status code and message
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        fp_item = data['questions'][0]['id']

        # get the secode page item
        response = self.client().get('/questions?page=2')
        data = json.loads(response.data)
         # check status code and message
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        data = json.loads(response.data)
        sp_item = data['questions'][0]['id']
        self.assertNotEqual(fp_item,sp_item)

    def test_get_invalid_page_questions(self):
        # print("****** runtest test_get_invalid_page_questions")
        # get the secode page item
        response = self.client().get('/questions?page=100')
        data = json.loads(response.data)
        # check status code and message
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)

    def test_post_question_withMissingField(self):
        # print("****** runtest test_post_question_withMissingField")

        # create new question without json data, then load response data
        data = {}
        data['question'] = "dummy question"
        data['answer'] = "ans"

        response = self.client().post('/questions', json=data)
        data = json.loads(response.data)
        # check status code and message
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['success'], False)

    # test post, search, get, delete in sequence
    def test_a_test_post_valid_question(self):
        # print("****** runtest test_a_test_post_valid_question")
        data = {}
        data['question'] = self.question_str
        data['answer'] = "ans"
        data['category'] = "5"
        data['difficulty'] = '1'

        response = self.client().post('/questions', json=data)
        data = json.loads(response.data)
        # check status code and message
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        if response.status_code == 200:
            self.cur_question_id = data['question']['id']
            # print(f" self.cur_question_id:{self.cur_question_id}")
    
    def test_b_test_search_question(self):
        # print("****** runtest test_b_test_search_question")
        if not self.cur_question_id:
            data = {}
            data['searchTerm'] = self.question_str
            response = self.client().post(f'/questions/search', json=data)
            data = json.loads(response.data)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(data['success'], True)
            self.assertGreater(data['totalQuestions'],0)
        else:
            self.assertIsNotNone(self.cur_question_id)
        
    def test_c_test_get_question(self):
        # print("****** runtest test_c_test_get_question")
        data = {}
        data['searchTerm'] = self.question_str
        response = self.client().post(f'/questions/search', json=data)
        data = json.loads(response.data)
        if response.status_code == 200:
            question_id = data['questions'][0]['id']
            # print(f"question_id:{question_id}")
            response = self.client().get(f'/questions/{question_id}')
            data = json.loads(response.data)
            # check status code and message
            self.assertEqual(response.status_code, 200)
            self.assertEqual(data['success'], True)
        else:
            self.assertTrue(False)

    def test_d_test_delete_question(self):
        # print("****** runtest test_c_test_get_question")
        data = {}
        data['searchTerm'] = self.question_str
        response = self.client().post(f'/questions/search', json=data)
        data = json.loads(response.data)
        if response.status_code == 200:
            question_id = data['questions'][0]['id']
            print(f"question_id:{question_id}")
            response = self.client().delete(f'/questions/{question_id}')
            data = json.loads(response.data)
            # check status code and message
            self.assertEqual(response.status_code, 200)
            self.assertEqual(data['success'], True)
        else:
            self.assertTrue(False)


    
    def test_get_nonexist_question(self):
        # print("****** runtest test_get_nonexist_question")
        response = self.client().get(f'/questions/9999')
        data = json.loads(response.data)
        # check status code and message
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)

    def test_delete_nonexist_question(self):
        # print("****** runtest test_delete_nonexist_question")
        response = self.client().delete(f'/questions/9999')
        data = json.loads(response.data)
        # check status code and message
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
    
    def test_post_quiz(self):
        category_id = 2
        data = {}
        data['quiz_category'] = {'id':category_id}
        data['previous_questions'] = []
        response = self.client().post('/quizzes', json=data)
        data = json.loads(response.data)
        # check status code and message
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertIsNotNone(data.get('question',None))









if __name__ == "__main__":
# Make the tests conveniently executable
    unittest.main()