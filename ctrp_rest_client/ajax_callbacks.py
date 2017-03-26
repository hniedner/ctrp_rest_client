from flask import jsonify, request
from ctrp_rest_client import app, api_client
from ctrp_rest_client import terminology


@app.route('/get_nr_of_trials')
def get_nr_of_trials():
    domain = request.args.get('dom')
    code = request.args.get('code')
    codes = terminology.get_subtree_codes(code)
    search_param = {}
    if 'disease' == domain:
        search_param['diseases.nci_thesaurus_concept_id'] = codes
    elif 'biomarker' == domain:
        search_param['biomarkers.nci_thesaurus_concept_id'] = codes
    else:
        return jsonify(0)
    return jsonify(api_client.get_nr_of_trials(search_param))


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


@app.route('/process_datatable_callback', methods=['POST'])
def process_datatable_callback():

    draw = request.values.get('draw', type=int)
    start = request.values.get('start', type=int)
    length = request.values.get('length', type=int)
    # search = request.values.get('search', type=list)
    # order = request.values['order']
    # columns = request.values['columns']

    search_params = {
        'eligibility.structured.gender': 'male'
    }

    result = api_client.find_trials(api_client.add_included_fields(search_params), start, length)

    result['draw'] = draw
    result['recordsFiltered'] = result['recordsTotal']
    # result['error'] = 'there was an error'
    return jsonify(result)


def _process_route(request_param, function_name):
    value = request.args.get(request_param)
    result = function_name(value)
    return jsonify(result)
