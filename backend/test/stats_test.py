from backend.utils.data_utils import get_results_for_minutes

if __name__ == '__main__':
    date_from = '2021-07-28 11:01:00'
    date_to = '2021-07-28 11:04:00'
    results = get_results_for_minutes(date_from=date_from, date_to=date_to)
    print(results)
