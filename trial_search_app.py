from flask import Flask, render_template, json
from flask_bootstrap import Bootstrap
from flask_nav import Nav

import api_client

# Initialize the Flask application
app = Flask(__name__)
app.debug = True

# Install our Bootstrap extension
Bootstrap(app)
# We initialize the navigation as well
nav = Nav()
nav.init_app(app)


@app.route('/')
def index():
    # retrieving trial as dictionary from the CTRP API client
    trial_dict = api_client.get_trial_by_nct_id('NCT02194738')

    # Convert json to python object
    trial_json = json.dumps(trial_dict)

    # Render template
    return render_template('index.html', trial=trial_dict)


# Run Flask webapp
if __name__ == '__main__':
    app.run()
