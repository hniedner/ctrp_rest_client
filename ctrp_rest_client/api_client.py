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

def find_all_trials(search_params):
    return find_trials(search_params, 0, 0, True)


def find_trials(search_params, start, length, fetch_all=False):
    search_params["from"] = start if start else 0
    search_params["size"] = 50 if fetch_all or length > 50 else length

    # shaping the dictionary to suit jquery datatables
    result = {
        "recordsTotal": -1,
        "data": []
    }

    while start < result['recordsTotal'] or result['recordsTotal'] < 0:
        start = _fetch_results(start, search_params, result)
        if fetch_all is False:  # no aggregation needed/wanted
            break

    # sanitize search_params
    search_params.pop('from', None)
    search_params.pop('size', None)
    search_params["returned"] = result['recordsTotal']
    return result


def _fetch_results(start, search_params, result):
    search_params['from'] = start
    draw = _call_api(search_params, 'clinical-trials?')
    if draw:
        result['data'].extend(draw['trials'])
        result['recordsTotal'] = draw['total']
        start += 50  # max number of retrieved record supported
    else:
        result['recordsTotal'] = 0
    return start


# return the total number of trials found matching
# the submitted search paramters
def get_nr_of_trials(search_params):
    result = _call_api(search_params)
    return result['total']


# default columns/fields to be displayed for the search results
cols = [
        "nci_id",
        "nct_id",
        "phase.phase",
        "start_date",
        "current_trial_status",
        "official_title"
    ]


# add the returned field to search_params
def add_included_fields(search_params, fields=cols):
    retval = search_params if search_params else {}
    retval['include'] = fields
    return retval


# returns terms values
def search_terms(query, size=20):
    search_params = dict()
    search_params['term'] = query
    search_params['size'] = size
    return _call_api(search_params, 'terms?')


# call clinical trials API and retrieves results and total number of results
def _call_api(search_params, url_ext='clinical-trials?'):
    req_url = urljoin(base_url, url_ext)
    log.debug('POST requesting: {}'.format(req_url))
    trials_retval = None

    try:
        log.debug('retrieving: ' + req_url)
        resp = requests.post(req_url, json=search_params, timeout=3)  # wait 3s for response
        log.info('Status Code: {}'.format(resp.status_code))

        if resp.status_code != 200:
            # This means something went wrong.
            log.warning(' Search for trials returned: {} \n {}'.format(resp.status_code, search_params))
        else:
            trials_retval = resp.json()

        return trials_retval

    except requests.exceptions.RequestException as e:
        log.error("error ", e)
