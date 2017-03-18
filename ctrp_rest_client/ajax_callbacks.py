from flask import jsonify, request
from ctrp_rest_client import app
from ctrp_rest_client import terminology

@app.route('/search_diseases')
def search_disease():
    return _process_route('q', terminology.search_cancertype_by_substring)


@app.route('/search_biomarkers')
def search_biomarker():
    return _process_route('q', terminology.search_biomarker_by_substring)


@app.route('/search_anatomicsites')
def search_anatomicsite():
    return _process_route('q', terminology.search_anatomicsite_by_substring)


@app.route('/search_drugs')
def search_drug():
    return _process_route('q', terminology.search_drug_by_substring)


@app.route('/search_diagnostic_test')
def search_diagnostic_test():
    return _process_route('q', terminology.search_diagnostic_procedure_by_substring)


@app.route('/search_lab_test')
def search_lab_test():
    return _process_route('q', terminology.search_laboratory_procedure_by_substring)


@app.route('/search_therapies')
def search_therapies():
    return _process_route('q', terminology.search_therapeutic_procedure_by_substring)


@app.route('/search_findings')
def search_finding():
    return _process_route('q', terminology.search_finding_by_substring)


@app.route('/search_diseases_associated_with_anatomic_site')
def search_diseases_associated_with_anatomic_site():
    return _process_route('code', terminology.search_diseases_associated_with_anatomic_site)


@app.route('/search_diseases_associated_with_finding')
def search_diseases_associated_with_finding():
    return _process_route('code', terminology.search_diseases_associated_with_finding)


@app.route('/search_diseases_associated_with_gene')
def search_diseases_associated_with_gene():
    return _process_route('code', terminology.search_diseases_associated_with_gene)


@app.route('/search_diseases_is_stage')
def search_diseases_is_stage():
    return _process_route('code', terminology.search_diseases_is_stage)


@app.route('/search_diseases_is_grade')
def search_diseases_is_grade():
    return _process_route('code', terminology.search_diseases_is_grade)


@app.route('/get_subtree_codes')
def get_subtree_codes():
    return _process_route('code', terminology.get_subtree_codes)


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
