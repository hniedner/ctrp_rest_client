import logging
from urllib.parse import urljoin

import requests

log = logging.getLogger(__name__)

# NCI Clinical Trials API Base URL
base_url = 'https://clinicaltrialsapi.cancer.gov/v1/'


# retrieve a clinical trial by NCT ID

def get_trial_by_nct_id(nct_id):
    req_url = urljoin(urljoin(base_url, 'clinical-trial/'), nct_id)
    log.warning('GET requesting: {}'.format(req_url))
    trial_retval = None

    try:
        resp = requests.get(req_url)
        log.info('Status Code: {}'.format(resp.status_code))

        if resp.status_code != 200:
            # This means something went wrong.
            log.warning(' Get trial for NCT {} returned: {}'.format(nct_id, resp.status_code))
        else:
            trial_retval = resp.json()

        return trial_retval

    except requests.exceptions.RequestException as e:
        log.error("error ", e)


# list of clinical trials based on search criteria
# review list of options at the online API documentation
# Bad hack to retrieve all records since API only returns
# 50 records at the time

def find_trials(search_params):
    start = 0  # start retrieving results from list index
    size = 50  # max number of trials retrieved as limited by the api
    rv = _call_api(search_params)
    total = rv["total"]
    data = []
    search_params["size"] = size

    while start < total:
        search_params["from"] = start
        this_draw = _call_api(search_params)
        data.extend(this_draw["trials"])
        start += size

    # shaping the dictionary to suit jquery datatables
    result = {
        "recordsTotal": total,
        "data": data
    }

    # sanitize search_params
    search_params.pop('from', None)
    search_params.pop('size', None)
    search_params["returned"] = total
    return result


# return the total number of trials found matching
# the submitted search paramters
def get_nr_of_trials(search_params):
    result = _call_api(search_params)
    return result['total']

# call clinical trials API and retrieves results and total number of results

def _call_api(search_params):
    req_url = urljoin(base_url, 'clinical-trials?')
    log.debug('POST requesting: {}'.format(req_url))
    trials_retval = None

    try:
        resp = requests.post(req_url, json=search_params)
        log.info('Status Code: {}'.format(resp.status_code))

        if resp.status_code != 200:
            # This means something went wrong.
            log.warning(' Search for trials returned: {}'.format(resp.status_code))
        else:
            trials_retval = resp.json()

        return trials_retval

    except requests.exceptions.RequestException as e:
        log.error("error ", e)
