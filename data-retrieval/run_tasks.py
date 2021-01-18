from celery import group
from tasks import get_historical_day_for_symbol
from db import retrieve_earliest_date_for_symbol
import time
from datetime import datetime, timedelta

# To be run with docker exec
TICKER_LIST = os.environ.get('TICKER_LIST').split(',')

if __name__ == '__main__':
    d = datetime.now()
    for symbol in TICKER_LIST:
        earliest_date = retrieve_earliest_date_for_symbol(symbol)
        delta = d - datetime.strptime(earliest_date, "%Y%m%d %H:%M:%S")
        number_of_days = delta.days
        print('number_of_days: ', number_of_days)
        group(get_historical_day_for_symbol.s(symbol, (d - timedelta(days=(i+1)))) for i in range(number_of_days))()
        time.sleep(2)
