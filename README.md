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
## Download NCI Thesaurus in tab-delimited format https://cbiit.nci.nih.gov/evs-download/thesaurus-downloads/
## Download and Install DB Browser for SQLite from http://sqlitebrowser.org/
## Create the Sqlite3 database for the NCI Thesaurus
    sqlite3 ncit # opens sqlite shell and create db ncit
## in the sqlite shell create the table for the thesaurus flat export
    create table terms (code CHARACTER(10), 
                        concept_name VARCHAR(255), 
                        parents VARCHAR(255), 
                        synonyms TEXT,
                        definition text, 
                        other_name TEXT, 
                        retired_concept TEXT, 
                        type VARCHAR(120));
                        
                        
# Run the application #
In order to run the application you need to export an environment variable that 
tells Flask where to find the application instance:

    export FLASK_APP=yourapplication

If you are outside of the project directory make sure to provide the exact path to your application directory. 
Similarly you can turn on “debug mode” with this environment variable:

    export FLASK_DEBUG=true

In order to install and run the application you need to issue the following commands:

    pip install -e .
    flask run