from flask import request, current_app,jsonify, make_response, abort
#  methods to process data in the model
DATA_PER_PAGE = 10
def paginate(request, data):
    page = request.args.get('page', 1, type=int)
    data_length = len(data)
    start = (page - 1) * DATA_PER_PAGE
    end = min(start + DATA_PER_PAGE, data_length -1)
    if (start > data_length-1):
        return []
    current_app.logger.info(f"start index:{start} end index: {end}")
    if start == end:
        current_data = data[start]
    else:
        current_data = data[start:end]

    return current_data

def check_require(require, data):
    # return empty list on succuss
    error_list = []
    
    for field in require:
        if field not in data:
            error_list.append(f"required field:{field} is not provided")
    return error_list

def error_response(status_code, message):
    data = jsonify({
        "success": False,
        "error": status_code,
        "message": message
    })
    response = make_response(data,status_code)
    return response

def error_data(status_code, message):
    data = jsonify({
        "success": False,
        "error": status_code,
        "message": message
    })
    return data