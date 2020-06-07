from flask_restful import Resource, reqparse
from models import db, Question, Category
from flask import current_app, abort, jsonify,request
import sys
from flaskr.dataproc import paginate, check_require,error_data, make_response, error_response

class QuestionResource(Resource):
    def get(self):
        error = False
        category_id = request.args.get('category_id', type = int, default = None)
        current_app.logger.info(f"category_id param value:{category_id}")
        try:
            # get catagories
            categories = Category.query.all()
            categories_dict = {}
            for category in categories:
                categories_dict[category.id] = category.type

            # get question
            if not category_id:
                questions = Question.query.order_by(Question.id).all()
                current_category = "all"
            else:
                questions = Question.query.order_by(Question.id).filter_by(category=category_id).all()
                current_category = categories_dict[category_id]
            
            data = [item.format() for item in questions]
            current_page_data = paginate(request, data)
            if not current_page_data:
                # response = make_response(error_data(404,"User give an invalid page number"),404)
                return error_response(404,"User give an invalid page number")
            
            
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
        
        return jsonify({
            'success': True,
            'questions': current_page_data,
            'total_questions':len(data),
            'categories': categories_dict,
            'current_category': current_category
        })

    def post(self):
        error = False
        json = request.get_json()
        error_list = check_require(['question','answer','category','difficulty'], json)
        if error_list:
            abort(400, jsonify({
                "error_list":error_list
            }))
        try:
            data = {}
            data['question'] = json.get('question')
            data['answer'] = json.get('answer')
            data['category'] = json.get('category')
            data['difficulty'] = json.get('difficulty')
            new_question = Question(**data)
            
            new_question.insert()
            question_data = new_question.format()
            current_app.logger.info(f'data:{question_data}')
            new_id = new_question.id
            # question_data = new_question.format()
        except:
            error = True
            db.session.rollback()
            errMsg = sys.exc_info()
            current_app.logger.error(errMsg)
        finally:
            db.session.close()
        
        if error:
            abort(500,errMsg)
        
        return jsonify({
            'success': True,
            'message': f"successfully add new question with id:{new_id}",
            "question": question_data
        })

class QuestionId(Resource):
    def get(self,id):
        error = False
        try:
            question = Question.query.filter_by(id=id).first()
            if not question:
                return error_response(404, f"Question with id:{id} cannot be found")
            data = question.format()
        except:
            error = True
            db.session.rollback()
            errMsg = sys.exc_info()
            current_app.logger.error(errMsg)
        finally:
            db.session.close()
        
        if error:
            abort(500,errMsg)
        
        return jsonify({
            'success': True,
            'question': data
        })

    def delete(self,id):
        error = False
        try:
            question = Question.query.filter_by(id=id).first()
            if not question:
                return error_response(404, f"Question with id:{id} cannot be found")
            question.delete()
        except:
            error = True
            db.session.rollback()
            errMsg = sys.exc_info()
            current_app.logger.error(errMsg)
        finally:
            db.session.close()
        
        if error:
            abort(500,errMsg)
        
        return jsonify({
            'success': True,
            'message': f"Question with id:{id} is successfully deleted"
        })

class QuestionSearch(Resource):
    def post(self):
        error = False
        json = request.get_json()
        
        if json:
            search_term = json.get("searchTerm","")
        else:
            search_term = ""

        looking_for = f"%{search_term}%"
        print(f"search_term:{looking_for}")

        try:
             # get catagories
            categories = Category.query.all()
            categories_dict = {}
            for category in categories:
                categories_dict[category.id] = category.type

            # questions = Question.query.filter(Question.question.ilike(looking_for)).all()
            questions = Question.query.filter(
                Question.question.ilike(looking_for)).all()
            data = [item.format() for item in questions]
            print(data)
            current_page_data = paginate(request, data)
        except:
            error = True
            db.session.rollback()
            errMsg = sys.exc_info()
            current_app.logger.error(errMsg)
        finally:
            db.session.close()
        
        if error:
            abort(500,errMsg)

        return jsonify({
            'success': True,
            'categories': categories_dict,
            'questions': current_page_data,
            'totalQuestions':len(data),
            'current_category':'all'
        })