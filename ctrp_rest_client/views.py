from flask import render_template, request,redirect, url_for

from ctrp_rest_client import app, api_client
from ctrp_rest_client.forms import TrialSearchForm


# home page - redirecting straight to search form
@app.route('/')
def home():
    # Render template
    return render_template('home.html')


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

        # calling the API
        result = api_client.find_trials(search_params)
        return render_template('display_results.html', search_params=search_params, result=result)

    # Render template
    return render_template('search_form.html', form=form)


def _parse_search_params(form):
    search_params = {
        "include": [
            "nci_id",
            "nct_id",
            "phase.phase",
            "start_date",
            "current_trial_status",
            "official_title"
        ]
    }

    if form.disease_codes.data:
        search_params["diseases.nci_thesaurus_concept_id"] = form.disease_codes.data
    if form.accepts_healthy_volunteers_indicator.data != 'NA':
        search_params["accepts_healthy_volunteers_indicator"] = form.accepts_healthy_volunteers_indicator.data
    if form.gender.data != 'Any':
        search_params["eligibility.structured.gender"] = form.gender.data
    if form.min_age_number.data:
        search_params["eligibility.structured.min_age_number_gte"] = form.min_age_number.data
    if form.max_age_number.data:
        search_params["eligibility.structured.max_age_number_lte"] = form.max_age_number.data

    disease_codes = _parse_list_values(form.disease_codes)
    if disease_codes:
        search_params["diseases.nci_thesaurus_concept_id"] = disease_codes

    biomarker_codes = _parse_list_values(form.biomarker_codes)
    if biomarker_codes:
        search_params["biomarkers.nci_thesaurus_concept_id"] = biomarker_codes

    assay_purposes = _parse_biomarker_assay_purpose(form)
    if assay_purposes:
        search_params["biomarkers.assay_purpose"] = assay_purposes

    phases = _parse_phase(form)
    if phases:
        search_params["phase.phase"] = phases

    print(search_params)

    return search_params


def _parse_list_values(formfield):
    items = []
    if formfield.data:
        items = [x.strip() for x in formfield.data.split(',')]

    print(items)
    return items


def _parse_biomarker_assay_purpose(form):
    assay_purposes = []
    if form.biomarker_assay_purpose_inclusion.data:
        assay_purposes.append('Eligibility Criterion - Inclusion')
    if form.biomarker_assay_purpose_exclusion.data:
        assay_purposes.append('Eligibility Criterion - Exclusion')

    return assay_purposes


def _parse_phase(form):
    phases = []
    if form.phasena.data:
        phases.append('NA')
    if form.phase0.data:
        phases.append('0')
    if form.phase1.data:
        phases.extend(['I', 'I_II'])
    if form.phase2.data:
        phases.extend(['II', 'II_III'])
        if 'I_II' not in phases:
            phases.append('I_II')
    if form.phase3.data:
        phases.append('III')
        if 'II_III' not in phases:
            phases.append('II_III')
    if form.phase4.data:
        phases.append('IV')

    return phases
