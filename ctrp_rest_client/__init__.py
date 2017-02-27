from flask import Flask
from flask_bootstrap import Bootstrap
from flask_bower import Bower

from ctrp_rest_client.config import configure_app

# Initialize the Flask application
app = Flask(__name__)

# Install our Bootstrap extension
Bootstrap(app)
# Install Bower extension
Bower(app)

configure_app(app)

# Pulling in the routes
import ctrp_rest_client.views
import ctrp_rest_client.ajax_callbacks