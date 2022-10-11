import datetime
import json
import logging
import random
from typing import Dict, Tuple, List

from bson import json_util
from flask import Flask, jsonify, request, Response

from backend.config.app_config import API_KEY, API_URL, ApiEndpoint, dao
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
    apikey = request.headers.get('x-api-key', '')
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
    json_request = request.get_json()
    start_datetime = datetime.datetime.now()
    # faccio controlli sui due campi
    if type(json_request.get('key')) == int or type(json_request.get('key')) == float \
            and json_request.get('key') in range(1, 7) \
            and type(json_request.get('payload')) == str and len(json_request.get('payload')) in range(10, 256):
        # Gestisco creation_datetime
        json_request['creation_datetime'] = start_datetime.strftime("%Y-%m-%d %H:%M:%S.%f")
        # Gestisco response_code
        json_request['response_code'] = random.choices(population=[200, 500], weights=(90, 10), k=1)[0]
        # Gestisco response_time
        end_datetime = datetime.datetime.now()
        response_time = (end_datetime - start_datetime).microseconds
        if response_time in range(10, 51):
            json_request['response_time'] = response_time
            dao.save(elem=json_request)
        else:
            raise TimeoutError('Timeout error')
    else:
        raise ValueError("Wrong parameters")
    # ritorno il json con tutti i dati
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
    date_from = request.args.get('date_from')
    date_to = request.args.get('date_to')
    results_for_minutes = get_results_for_minutes(date_from=date_from, date_to=date_to)
    # faccio statistiche sui valori ritornati
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
