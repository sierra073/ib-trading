from celery import group
from tasks import get_historical_day_for_symbol
from db import retrieve_earliest_date_for_symbol
import time
from datetime import datetime, timedelta

# To be run with docker exec

if __name__ == '__main__':
    d = datetime.now()
    earliest_date = retrieve_earliest_date_for_symbol('SPY')

    delta = d - datetime.strptime(earliest_date, "%Y%m%d %H:%M:%S")
    number_of_days = delta.days
    print('number_of_days: ', number_of_days)
    group(get_historical_day_for_symbol.s('SPY', (d - timedelta(days=(i+1)))) for i in range(number_of_days))()
