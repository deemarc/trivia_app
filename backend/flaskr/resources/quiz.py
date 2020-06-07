from flask_restful import Resource, reqparse
from models import db, Question, Category
from flask import current_app, abort, jsonify,request
import sys
from flaskr.dataproc import paginate, check_require,error_data, make_response, error_response

import random

def random_question(quiestion_list, pre_q):
    q_len = len(quiestion_list)
    pre_q_len = len(pre_q)
    if pre_q_len == q_len:
        return []

    for i in range(0,q_len):
        rand_index = random.randint(0,q_len-1-i)
        if quiestion_list[rand_index]['id'] in pre_q:
            pop_q = quiestion_list.pop(rand_index)
            current_app.logger.info(f"pop_q:{pop_q}")
            continue
        else:
            return quiestion_list[rand_index]

    return []


class QuizeResource(Resource):
    def post(self):
        error = False
        json = request.get_json()
        category = json.get('quiz_category',None)
        if category:
            category_id = int(category.get('id'))
        else:
            category_id = 0
        
        pre_q = json.get('previous_questions',[])

        # print(f"pre_q:{pre_q}")

        try:
            # get catagories
            
            categories = Category.query.all()
            categories_dict = {}
            for category in categories:
                categories_dict[category.id] = category.type

            # get question
            if category_id == 0:
                questions = Question.query.order_by(Question.id).all()
                current_category = "all"
            else:
                questions = Question.query.order_by(Question.id).filter_by(category=category_id).all()
                current_category = categories_dict[category_id]
            
            question_list = [item.format() for item in questions]

            rand_q = random_question(question_list, pre_q)

            
            
            # cat_data = [item.format() for item in categories]
            # current_type = cat_data[0]['id']
            # if not current_page_data:
            #     return json_abort(404,"User give an invalid page number")
        except:
            error = True
            db.session.rollback()
            errMsg = sys.exc_info()
            current_app.logger.error(errMsg)
        finally:
            db.session.close()
        
        if error:
            abort(500,errMsg)

        # random question return empty list meaning all questions in that category have bee played
        if not rand_q:
            return jsonify({
                'success': True
            })
        
        return jsonify({
            'success': True,
            'question': rand_q,
            'current_category':current_category
        })
