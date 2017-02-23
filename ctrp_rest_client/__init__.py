from flask import Flask
from flask_bootstrap import Bootstrap

# Initialize the Flask application
app = Flask(__name__)
app.secret_key = 'ctrp'

# Install our Bootstrap extension
Bootstrap(app)

# Pulling in the routes
import ctrp_rest_client.views
import ctrp_rest_client.ajax_callbacks