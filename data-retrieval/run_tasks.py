from celery import group
from tasks import get_historical_day_for_symbol
from market_reader_historical import MarketReaderHistorical
import time
from datetime import datetime, timedelta

# To be run with docker exec

# this is here temporarily, ideally run a batch process to one-time store all the earliest dates for symbols in a table
# def get_earliest_date(client, contract):
#     return client.reqHeadTimeStamp(4101, contract, 'TRADES', 0, 1)

if __name__ == '__main__':
    d = datetime.now()
    earliest_date = datetime(2020, 12, 28)
    # client = MarketReaderHistorical('127.0.0.1', 4002, 0)
    # contract = Contract()
    # contract.symbol = symbol
    # contract.secType = 'STK'
    # contract.exchange = 'SMART'
    # contract.currency = 'USD'
    # earliest_date = datetime.strptime(get_earliest_date(client, contract), "%Y%m%d %H:%M:%S")
    # client.disconnect()

    delta = d - earliest_date
    number_of_days = delta.days
    print('number_of_days: ', number_of_days)
    group(get_historical_day_for_symbol.s('SPY', (d - timedelta(days=(i+1)))) for i in range(number_of_days))()
