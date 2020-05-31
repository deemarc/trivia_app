from flask_restful import Resource, reqparse
from models import db, Category
from flask import current_app, abort, jsonify
import sys

class CategoryResource(Resource):
    def get(self):
        error = False
        try:
            categories = Category.query.all()
            print('done')
            data = [item.format() for item in categories]
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
            'categories': data
        })