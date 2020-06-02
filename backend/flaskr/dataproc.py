from flask import request, current_app
#  methods to process data in the model
DATA_PER_PAGE = 10
def paginate(request, data):
    page = request.args.get('page', 1, type=int)
    
    start = (page - 1) * DATA_PER_PAGE
    end = start + DATA_PER_PAGE
    current_app.logger.info(f"start index:{start} end index: {end}")
    current_data = data[start:end]

    return current_data

def check_require(require, data):
    # return empty list on succuss
    error_list = []
    
    for field in require:
        if field not in data:
            error_list.append(f"required field:{field} is not provided")
    return error_list
            