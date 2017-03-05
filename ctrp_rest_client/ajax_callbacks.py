from flask import jsonify, request
from ctrp_rest_client import app
from ctrp_rest_client import terminology


@app.route('/search_diseases')
def search_disease():
    return _process_route('q', terminology.search_cancertypes_by_substring)


@app.route('/search_biomarkers')
def search_biomarkers():
    return _process_route('q', terminology.search_biomarkers_by_substring)


@app.route('/get_child_codes')
def get_child_codes():
    return _process_route('code', terminology.get_child_codes)


@app.route('/get_parent_codes')
def get_parent_codes():
    return _process_route('code', terminology.get_parent_codes)


@app.route('/get_name_for_code')
def get_name_for_code():
    domain = request.args.get('dom')
    code = request.args.get('code')
    name = terminology.get_name_for_code(domain, code)
    return jsonify(name)


def _process_route(request_param, function_name):
    value = request.args.get(request_param)
    result = function_name(value)
    return jsonify(result)