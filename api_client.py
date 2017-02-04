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


def find_trials(search_params):
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
