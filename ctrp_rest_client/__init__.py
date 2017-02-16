from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap

from ctrp_rest_client.static import api_client
from forms import TrialSearchForm

# Initialize the Flask application
app = Flask(__name__)
app.secret_key = 'ctrp'
app.debug = True

# Install our Bootstrap extension
Bootstrap(app)


# home page - redirecting straight to search form
@app.route('/')
def home():
    # Render template
    return render_template('home.html')


# display information for the trial identified by the nct_id (or nci id)
@app.route('/show_trial', methods=['POST'])
def show_trial():
    # parse form parameter
    trial_id = request.form["trial_id"]
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

    if form.disease_code.data:
        search_params["diseases.nci_thesaurus_concept_id"] = form.disease_code.data
    if form.accepts_healthy_volunteers_indicator.data != 'NA':
        search_params["accepts_healthy_volunteers_indicator"] = form.accepts_healthy_volunteers_indicator.data
    if form.gender.data != 'Any':
        search_params["eligibility.structured.gender"] = form.gender.data

    phases = _parse_phase(form)
    if phases:
        search_params["phase.phase"] = phases

    return search_params


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

# Run Flask webapp
if __name__ == '__main__':
    app.run()
