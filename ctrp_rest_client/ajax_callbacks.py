from flask import jsonify, request, json

import terminology
from ctrp_rest_client import app, api_client
from gis_service import ZipCodeService


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


@app.route('/get_root_concept')
def get_root_concept():
    return _process_route(['dom'], terminology.get_root_concept)


@app.route('/search_terminology')
def search_domain_by_substring():
    return _process_route(['dom', 'q'], terminology.search_domain_by_substring)


@app.route('/search_diseases_associated_with_anatomicsite')
def search_diseases_associated_with_anatomic_site():
    return _process_route(['code'], terminology.search_diseases_associated_with_anatomic_site)


@app.route('/search_diseases_associated_with_finding')
def search_diseases_associated_with_finding():
    return _process_route(['code'], terminology.search_diseases_associated_with_finding)


@app.route('/search_diseases_associated_with_gene')
def search_diseases_associated_with_gene():
    return _process_route(['code'], terminology.search_diseases_associated_with_gene)


@app.route('/search_diseases_is_stage')
def search_diseases_is_stage():
    return _process_route(['code'], terminology.search_diseases_is_stage)


@app.route('/search_diseases_is_grade')
def search_diseases_is_grade():
    return _process_route(['code'], terminology.search_diseases_is_grade)


@app.route('/get_subtree_codes')
def get_subtree_codes():
    return _process_route(['code', 'dom'], terminology.get_subtree_codes)


@app.route('/get_child_codes')
def get_child_codes():
    return _process_route(['code', 'dom'], terminology.get_child_codes)


@app.route('/get_parent_codes')
def get_parent_codes():
    return _process_route(['code', 'dom'], terminology.get_parent_codes)


@app.route('/search_terms')
def search_terms():
    query = request.args.get('q')
    size = request.args.get('size')
    retval = api_client.search_terms(query, size)
    terms = []
    if retval:
        terms = retval['terms']
    return jsonify(terms)


@app.route('/process_datatable_callback', methods=['POST'])
def process_datatable_callback():

    draw = request.values.get('draw', type=int)
    start = request.values.get('start', type=int)
    length = request.values.get('length', type=int)
    search_val = request.values.get('search[value]', type=str)

    if search_val:
        search_params = {**api_client.add_included_fields({}), **json.loads(search_val)}
    else:
        search_params = api_client.add_included_fields({})

    fetch_all = False
    if -1 == length:
        length = 50
        fetch_all = True

    result = api_client.find_trials(search_params, start, length, fetch_all)
    result['draw'] = draw
    result['recordsFiltered'] = result['recordsTotal'] if result['recordsTotal'] else 0
    # result['error'] = 'there was an error'
    return jsonify(result)


def _process_route(request_param, function_name):
    values = []
    for param in request_param:
        values.append(request.args.get(param))
    result = function_name(*values)
    return jsonify(result)


zcs = ZipCodeService()


@app.route('/get_zip_coords')
def get_zip_coords():
    zip_code = request.args.get('zip_code')
    return jsonify(zcs.get_coords(zip_code))
