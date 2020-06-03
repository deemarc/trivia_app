from flask_restful import Resource, reqparse
from models import db, Question
from flask import current_app, abort, jsonify,request
import sys
from flaskr.dataproc import paginate, check_require,error_data, make_response, error_response

class QuestionResource(Resource):
    def get(self):
        error = False
        try:
            questions = Question.query.order_by(Question.id).all()
            data = [item.format() for item in questions]
            current_page_data = paginate(request, data)
            if not current_page_data:
                # response = make_response(error_data(404,"User give an invalid page number"),404)
                return error_response(404,"User give an invalid page number")

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
            'total_questions':len(data)
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

        # incomping param
        req_dict = request.args.to_dict()

        search_str = req_dict.get("search_term","")
        looking_for = f"%{search_str}%"

        try:
            questions = Question.query.filter(Question.question.ilike(looking_for))
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
            'matched_questions': current_page_data,
            'total_matched_questions':len(data)
        })