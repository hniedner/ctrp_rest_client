# ctrp_rest_client
Example client for the NCI Clinical Trial Search RESTful API

# Setup #
The application currently uses a local sqlite database that provides parsed
information from the NCI Thesaurus. Plans are to switch this to use NCI EVS provided 
web services.
## Install Python 3
## Create virtual Python environment
    python3 -m venv venv # creates virtual environment in directory venv in the current directory
## Activate your virtual environment
    source venv/bin/activate
## Install required python packages (modules)
    pip3 install -r requirements.txt
## In order to use the sqlite3 module in python you either need to copy the sqllite3 module directory
from your system python installation to your virtual environment's library directory or
install the virtual environment to use the system libraries.
see more: http://stackoverflow.com/questions/23181197/install-pysqlite-in-virtualenv-with-python3-support
use parameter when creating the virtual Python environment: --system-site-packages
see more at: https://docs.python.org/3/library/venv.html
## Install Bower to install and manage javascript libraries
    https://bower.io/
## Install javascript resources from bower.json with Bower
    cd ctrp_rest_client
    bower install
   
# Run the application #
In order to run the application you need to export an environment variable that 
tells Flask where to find the application instance:

    export FLASK_APP=ctrp_rest_client

If you are outside of the project directory make sure to provide the exact path to your application directory. 
Choose an application configuration (default, testing, development) in the config.py:

    export FLASK_CONFIGURATION=development

In order to install and run the application you need to issue the following commands:

    pip install -e .
    flask run
    
Alternatively you can also use a run configuration for run.py which is handy for
IDE such as PyCharm.