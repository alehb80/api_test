import datetime
from collections import OrderedDict
from datetime import timedelta
from typing import List

from backend.config.app_config import odm


def get_stats_logs(date_from: str, date_to: str) -> List:
    """
    It takes a date range and returns the last 10 logs in that range

    :param date_from: The date from which you want to get the logs
    :type date_from: str
    :param date_to: The date and time to which you want to get the logs
    :type date_to: str
    :return: A list of the last 10 logs
    """
    date_to = date_to.replace('-', '/')
    date_to = datetime.datetime.strptime(date_to, "%Y/%m/%d %H:%M:%S")
    date_to = date_to + timedelta(minutes=1)
    date_to = date_to.strftime("%Y-%m-%d %H:%M:%S.%f")
    pipeline = [
        {
            "$match": {
                "creation_datetime": {
                    "$gte": date_from,
                    "$lte": date_to,
                },
            },
        },
        {
            "$sort": OrderedDict(
                [
                    ("creation_datetime", -1),

                ]
            )
        },
        {
            "$limit": 10
        },
    ]
    return list(odm.collection.aggregate(pipeline))
