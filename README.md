# ctrp_rest_client
Example client for the NCI CTRP RESTful API

# Setup #
## Install Python 3
## Create virtual Python environment
    python -m venv venv # creates virtual environment in directory venv in the current directory
## Activate your virtual environment
    source venv/bin/activate
## Install required python packages (modules)
    pip install -r requirements.txt
## In order to use the sqlite3 module in python you either need to copy the sqllite3 module directory
from your system python installation to your virtual environment's library directory or
install the virtual environment to use the system libraries.
see more: http://stackoverflow.com/questions/23181197/install-pysqlite-in-virtualenv-with-python3-support
use parameter when creating the virtual Python environment: --system-site-packages
see more at: https://docs.python.org/3/library/venv.html
                        
# Run the application #
In order to run the application you need to export an environment variable that 
tells Flask where to find the application instance:

    export FLASK_APP=ctrp_rest_client

If you are outside of the project directory make sure to provide the exact path to your application directory. 
Similarly you can turn on “debug mode” with this environment variable:

    export FLASK_DEBUG=true

In order to install and run the application you need to issue the following commands:

    pip install -e .
    flask run