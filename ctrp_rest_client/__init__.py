import json

from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_nav import Nav
from flask_nav.elements import Navbar, View
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired

from ctrp_rest_client.static import api_client


class SimpleSearchForm(FlaskForm):
    nct_id = StringField('nct_id', validators=[DataRequired()])


# Initialize the Flask application
app = Flask(__name__)
app.secret_key = 'ctrp'
app.debug = True

# Install our Bootstrap extension
Bootstrap(app)

# We initialize the navigation as well
nav = Nav()


@nav.navigation()
def top_navbar():
    return Navbar(
        'NCI Clinical Trial Search', View('Home', 'home'),
    )
nav.init_app(app)


@app.route('/')
def home():
    return search_form()


@app.route('/display_trial/<string:nct_id>')
def display_trial(nct_id):
    # retrieving trial as dictionary from the CTRP API client
    trial_dict = api_client.get_trial_by_nct_id(nct_id)

    # Render template
    return render_template('display_trial.html', trial=trial_dict)


@app.route('/search_form', methods=('GET', 'POST'))
def search_form():
    form = SimpleSearchForm()
    if form.validate_on_submit():
        return redirect(url_for('display_trial', nct_id=form.nct_id.data))

    # Render template
    return render_template('search_form.html', form=form)


@app.route('/display_results')
def display_results():
    # Render template
    return render_template('display_results.html')


@app.route('/_get_data')
def _get_data():
    search_params = {
        "eligibility.structured.gender": "female",
        "include": ["nci_id", "nct_id", "phase.phase", "start_date", "current_trial_status", "official_title"]
    }
    # calling the API
    result = api_client.find_trials(search_params)

    # dump as json string
    data = json.dumps(result)
    return data


# Run Flask webapp
if __name__ == '__main__':
    app.run()
