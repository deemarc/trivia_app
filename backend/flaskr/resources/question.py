from flask_restful import Resource, reqparse
from models import db, Question
from flask import current_app, abort, jsonify,request
import sys
from flaskr.dataproc import paginate, check_require

class QuestionResource(Resource):
    def get(self):
        error = False
        try:
            questions = Question.query.order_by(Question.id).all()
            data = [item.format() for item in questions]
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
            new_id = new_question.id
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
            'message': f"successfully add new question with id:{new_id}"
        })

class QuestionId(Resource):
    def delete(self,id):
        error = False
        try:
            question = Question.query.filter_by(id=id).first()
            if not question:
                abort(404, f"Question with id:{id} cannot be found")
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
        search_str = request.get("search_term","")
        looking_for = f"%{search_str}%"

        try:
            questions = Question.query.filter(Venue.name.ilike(looking_for))
            total_questions = questions.count()
            data = [item.format() for item in questions]
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
            'total_matched_questions':total_questions
        })