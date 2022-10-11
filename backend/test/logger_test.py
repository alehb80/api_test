import logging

from backend.utils.logger_utils import get_stats_logs

if __name__ == '__main__':
    date_from = "2021-07-28 11:01:00"
    date_to = "2021-07-28 11:04:00"
    logs_values = get_stats_logs(date_from=date_from, date_to=date_to)
    logging.basicConfig(level=logging.DEBUG)
    logging.info("Ultimi 10 logs dell’ultima aggregazione nella finestra temporale.")
    for log_info in logs_values:
        logging.info(" -> {}, {}, {}, {}, {}".format(
            log_info.get('key'),
            log_info.get('payload'),
            log_info.get('response_time'),
            log_info.get('response_code'),
            log_info.get('creation_datetime')
        ))
