import os

from flask import render_template, request, redirect, url_for, send_from_directory

from ctrp_rest_client import app, api_client
from ctrp_rest_client.forms import TrialSearchForm


# home page - redirecting straight to search form
@app.route('/')
def home():
    # Render template
    return render_template('home.html')


@app.route('/live_search')
def test():
    # Render template
    return render_template('live_search.html')


# tree
@app.route('/tree')
def tree():
    # Render template
    return render_template('tree.html')


# favicon serving
@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static/img'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')


# display information for the trial identified by the nct_id (or nci id)
@app.route('/find_trial', methods=['POST'])
def find_trial():
    # parse form parameter
    trial_id = request.form["trial_id"]
    # Render template
    return redirect(url_for('display_trial', trial_id=trial_id))


# display information for the trial identified by the nct_id (or nci id)
@app.route('/display_trial/<trial_id>', methods=['GET'])
def display_trial(trial_id):
    # retrieving trial as dictionary from the CTRP API client
    trial_dict = api_client.get_trial_by_nct_id(trial_id)
    # Render template
    return render_template('display_trial.html', trial=trial_dict)


# display search form
@app.route('/search', methods=('GET', 'POST'))
def search():
    form = TrialSearchForm(request.form)
    if request.method == 'POST' and form.validate_on_submit():
        search_params = _parse_search_params(form)
        terms = _parse_terms(form)
        # calling the API
        result = api_client.find_trials(search_params)
        return render_template('display_results.html', search_params=search_params, result=result, terms=terms)

    # Render template
    return render_template('search_form.html', form=form)


# parse list of names for terminology based search fields
# these are for display only as the search is using the codes (concept ids)
def _parse_terms(form):
    terms = {}
    if form.disease_names.data:
        terms['disease_names'] = form.disease_names.data.split(', ')
    if form.biomarker_names.data:
        terms['biomarker_names'] = form.biomarker_names.data.split(', ')
    return terms


def _add_included_fields(search_params):
    search_params['include'] = [
        "nci_id",
        "nct_id",
        "phase.phase",
        "start_date",
        "current_trial_status",
        "official_title"
    ]
    return search_params


# extract values from form fields and populate the query for the
# search request to the API
def _parse_search_params(form):
    search_params = _add_included_fields({})

    if form.accepts_healthy_volunteers_indicator.data != 'NA':
        search_params["accepts_healthy_volunteers_indicator"] = form.accepts_healthy_volunteers_indicator.data

    if form.gender.data != 'Any':
        search_params["eligibility.structured.gender"] = form.gender.data

    _conditional_add_value(search_params, '_fulltext', form.fulltext.data)
    _conditional_add_value(search_params, 'eligibility.structured.min_age_number_gte', form.min_age_number.data)
    _conditional_add_value(search_params, 'eligibility.structured.max_age_number_lte', form.max_age_number.data)

    disease_codes = _parse_list_values(form.disease_codes)
    _conditional_add_value(search_params, 'diseases.nci_thesaurus_concept_id', disease_codes)

    biomarker_codes = _parse_list_values(form.biomarker_codes)
    _conditional_add_value(search_params, 'biomarkers.nci_thesaurus_concept_id', biomarker_codes)

    assay_purposes = _parse_biomarker_assay_purpose(form)
    _conditional_add_value(search_params, 'biomarkers.assay_purpose', assay_purposes)

    phases = _parse_phase(form)
    _conditional_add_value(search_params, 'phase.phase', phases)

    return search_params


def _conditional_add_value(target_dict, key, value):
    if value:
        target_dict[key] = value


def _parse_list_values(formfield):
    items = []
    if formfield.data:
        items = [x.strip() for x in formfield.data.split(',')]
    return items


def _parse_biomarker_assay_purpose(form):
    assay_purposes = []
    _conditional_add_to_list(assay_purposes, ['Eligibility Criterion - Inclusion'],
                             form.biomarker_assay_purpose_inclusion.data)
    _conditional_add_to_list(assay_purposes, ['Eligibility Criterion - Exclusion'],
                             form.biomarker_assay_purpose_exclusion.data)
    return assay_purposes


def _parse_phase(form):
    phases = []
    _conditional_add_to_list(phases, ['NA'], form.phasena.data)
    _conditional_add_to_list(phases, ['I', 'I_II'], form.phase1.data)
    _conditional_add_to_list(phases, ['I_II', 'II', 'II_III'], form.phase2.data)
    _conditional_add_to_list(phases, ['II_III', 'III'], form.phase3.data)
    _conditional_add_to_list(phases, ['IV'], form.phase4.data)
    return phases


def _conditional_add_to_list(target_list, values, form_value):
    if form_value:
        for value in values:
            if value not in target_list:
                target_list.append(value)
