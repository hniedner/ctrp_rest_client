from flask import jsonify, request
from ctrp_rest_client import app
from ctrp_rest_client import terminology


@app.route('/search_diseases')
def search_disease():
    query = request.args.get('q')
    result = terminology.search_cancertypes_by_substring(query)
    return jsonify(result)


@app.route('/search_biomarkers')
def search_biomarkers():
    query = request.args.get('q')
    result = terminology.search_biomarkers_by_substring(query)
    return jsonify(result)


@app.route('/expand_ncit_code')
def expand_ncit_code():
    code = request.args.get('code')
    result = terminology.expand_code_subtree(code)
    return jsonify(result)


@app.route('/get_name_for_ncit_code')
def get_name_for_ncit_code():
    domain = request.args.get('dom')
    code = request.args.get('code')
    name = terminology.get_name_for_code(domain, code)
    return jsonify(name)
