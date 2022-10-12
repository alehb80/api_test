import datetime
import json
import logging
import random
from typing import Dict, Tuple, List

from bson import json_util
from flask import Flask, jsonify, request, Response

from backend.config.app_config import API_KEY, API_URL, ApiEndpoint, odm
from backend.utils.data_utils import get_results_for_minutes
from backend.utils.logger_utils import get_stats_logs

app = Flask(
    "bigprofiles-api-frontend-test",
)

logging.basicConfig(level=logging.DEBUG)


@app.before_request
def check_authentication() -> Tuple[Response, int]:
    """
    If the request header contains an `x-api-key` key, and the value of that key is equal to the value of the `API_KEY`
    variable, then the request is allowed to proceed. Otherwise, the request is rejected with a 401 status code
    :return: A tuple of a response and an integer.
    """
    # Retrieving API-key from the request headers
    apikey = request.headers.get('x-api-key', '')
    # Check on the API-key for the authentication
    if apikey != API_KEY:
        return jsonify({'message': 'Authentication failed: the API key is not valid or missing in request.'}), 401


@app.route(API_URL + ApiEndpoint.API_ENDPOINT_INGEST.value, methods=['POST'])
def ingest_api_v1_ingest_post() -> Dict:
    """
    It takes a JSON object as input, checks if the key and payload fields are valid, then saves the object
    to the database.
    :return: a dictionary with the following keys:
        - key
        - payload
        - creation_datetime
        - response_code
        - response_time
    """
    # Retrieving parameters from the request
    json_request = request.get_json()
    # Setting the start time of the request
    start_datetime = datetime.datetime.now()
    # Checking the two json fields
    if type(json_request.get('key')) == int or type(json_request.get('key')) == float \
            and json_request.get('key') in range(1, 7) \
            and type(json_request.get('payload')) == str and len(json_request.get('payload')) in range(10, 256):
        # Saving the date and time of the request
        json_request['creation_datetime'] = start_datetime.strftime("%Y-%m-%d %H:%M:%S.%f")
        # Saving the code of the response
        json_request['response_code'] = random.choices(population=[200, 500], weights=(90, 10), k=1)[0]
        # Setting time delta of the request
        end_datetime = datetime.datetime.now()
        response_time = (end_datetime - start_datetime).microseconds
        # Checking if the time delta belongs to an interval from 10ms to 50ms
        if response_time in range(10, 51):
            # Saving the time of the response corresponds to time delta
            json_request['response_time'] = response_time
            # Saving data to database
            odm.save(elem=json_request)
        else:
            raise TimeoutError('Timeout error')
    else:
        raise ValueError("Wrong parameters")
    return json.loads(json_util.dumps(json_request))


@app.route(API_URL + ApiEndpoint.API_ENDPOINT_RETRIEVE.value, methods=['GET'])
def retrieve_api_v1_retrieve_get() -> List:
    """
    It retrieves the results for the given time interval
    :return: A list of dictionaries, each dictionary contains the following keys:
        - key: the key of the request
        - payload: the payload of the request
        - response_time: the response time of the request
        - response_code: the response code of the request
        - creation_datetime: the creation datetime of the request
    """
    # Retrieving parameters from the request
    date_from = request.args.get('date_from')
    date_to = request.args.get('date_to')
    # Retrieval of statistics grouped by minute and relating to the chosen time window
    results_for_minutes = get_results_for_minutes(date_from=date_from, date_to=date_to)
    # Logs display the list of the last 10 logs of the last aggregation in the time window.
    stats_logs = get_stats_logs(date_from=date_from, date_to=date_to)
    logging.info(" Ultimi 10 logs dell’ultima aggregazione nella finestra temporale.")
    for log_info in stats_logs:
        logging.info(" -> {}, {}, {}, {}, {}".format(
            log_info.get('key'),
            log_info.get('payload'),
            log_info.get('response_time'),
            log_info.get('response_code'),
            log_info.get('creation_datetime')
        ))
    return results_for_minutes


app.run(port=8000)
