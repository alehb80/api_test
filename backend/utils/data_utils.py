import datetime
from collections import OrderedDict
from datetime import timedelta
from typing import List

from backend.config.app_config import dao


def get_results_for_minutes(date_from: str, date_to: str) -> List:
    """
    It takes two dates, and returns a list of all the stats between those two dates

    :param date_from: The start date and time of the time period you want to get stats for
    :type date_from: str
    :param date_to: The date and time to which you want to get the results
    :type date_to: str
    :return: A list of lists of dictionaries.
    """
    date_from = date_from.replace('-', '/')
    date_to = date_to.replace('-', '/')
    date_from = datetime.datetime.strptime(date_from, "%Y/%m/%d %H:%M:%S")
    date_to = datetime.datetime.strptime(date_to, "%Y/%m/%d %H:%M:%S")
    date_to = date_to + timedelta(minutes=1)
    pipeline = [
        {
            "$project": {
                "creation_datetime": {
                    "$toDate": "$creation_datetime"
                },
                "key":               "$key",
                "response_time":     "$response_time",
                "payload":           "$payload",
                "response_code":     "$response_code",
            },
        },
        {
            "$match": {
                "creation_datetime": {
                    "$gte": date_from,
                    "$lte": date_to,
                },
            },
        },
        {
            "$group": {
                "_id":                    {
                    "interval": {
                        "$subtract": [
                            {"$minute": "$creation_datetime"},
                            {"$mod": [{"$minute": "$creation_datetime"}, 1]}
                        ]
                    },
                    "key":      "$key",
                },
                "total_requests":         {
                    "$sum": 1
                },
                "total_response_time_ms": {
                    "$sum": "$response_time"
                },
                "total_errors":           {
                    "$sum": {
                        "$switch": {
                            "branches": [
                                {
                                    "case": {
                                        "$eq": ["$response_code", 500]
                                    },
                                    "then": {"$sum": 1}
                                }
                            ],
                            "default":  0
                        }
                    }
                },
            },
        },
        {
            "$sort": OrderedDict([("_id.interval", 1), ("_id.key", 1)])
        },
    ]
    total_stats = list(dao.collection.aggregate(pipeline))
    return total_stats
