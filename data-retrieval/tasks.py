from ibapi.client import Contract
from market_reader_historical import MarketReaderHistorical
from datetime import datetime, timedelta
from dateutil import parser
import time
import pandas as pd
from sqlalchemy import create_engine
import os
from celery import Celery
from celery.utils.log import get_task_logger
DATABASE_URL = os.environ.get('DATABASE_URL')

app = Celery('tasks', broker='redis://redis:6379/0', backend='redis://redis:6379/0')

@app.task(autoretry_for=(Exception,), default_retry_delay=30, max_retries=10, acks_late=True)
def get_historical_day_for_symbol(symbol, day, **kwargs):
    client = MarketReaderHistorical('tws', 4004, 0)
    contract = Contract()
    contract.symbol = symbol
    contract.secType = kwargs.get('secType', 'STK')
    contract.exchange = kwargs.get('exchange', 'SMART')
    contract.currency = kwargs.get('currency', 'USD')
    retrieve_historical_30s_data(client, contract, day)
    # Disconnect from TWS
    client.disconnect()
    return 'success'

def retrieve_historical_30s_data(client, contract, day):
    request_30s_data(client, contract, day, 1)
    while len(client.data) == 0:
        time.sleep(1)
    result = pd.DataFrame.from_records(client.data)
    print(result.shape)
    print(result.head(2))
    insert_historical_data(result, contract.symbol)

def request_30s_data(client, contract, day, i):
    d = parser.parse(day)
    endDateTime = d.strftime("%Y%m%d %H:%M:%S")
    client.reqHistoricalData(i, contract, endDateTime, '1 D', '30 secs', 'TRADES', 1, 1, False, [])
    time.sleep(5)

def insert_historical_data(result, ticker):
    try:
        engine = create_engine(DATABASE_URL)
        result.to_sql('historical_data_' + ticker.lower(), con=engine, if_exists='append', index=False)
        print('inserted data for ' + ticker)
    except Exception:
        print('data already inserted for this time range')
        pass