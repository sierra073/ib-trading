from ibapi.client import Contract
from market_reader_historical import MarketReaderHistorical
from celery import app
from datetime import datetime, timedelta
import time
import pandas as pd
from sqlalchemy import create_engine
import os

DATABASE_URL = os.environ.get('DATABASE_URL')
print('DATABASE_URL: ' + DATABASE_URL)

@app.task(bind=True, default_retry_delay=20, max_retries=10, acks_late=True)
def get_historical_day_for_symbol(symbol, day):

    # Create the client and connect to IB Gateway
    client = MarketReaderHistorical('127.0.0.1', 4002, 0)

    contract = Contract()
    contract.symbol = symbol
    contract.secType = 'STK'
    contract.exchange = 'SMART'
    contract.currency = 'USD'

    retrieve_historical_30s_data(client, contract, day)

    # Disconnect from TWS
    client.disconnect()

def retrieve_historical_30s_data(client, contract, day):
    request_30s_data(client, contract, day, 1)

    if client.done:
        result = pd.DataFrame.from_records(client.data)
        print('data dimensions:', result.shape)
        insert_historical_data(result, contract.symbol)

def request_30s_data(client, contract, day, i):
    endDateTime = day.strftime("%Y%m%d %H:%M:%S")
    client.reqHistoricalData(i, contract, endDateTime, '1 D', '30 secs', 'TRADES', 1, 1, False, [])
    time.sleep(5)

def insert_historical_data(result, ticker):
    engine = create_engine(DATABASE_URL)
    print('inserting: ' + result)
    try:
        result.to_sql('historical_data_' + ticker.lower(), con=engine, if_exists='append', chunksize=1000, index=False)
        print('inserted data for ' + ticker)
    except IntegrityError:
        print('data already inserted for this time range')
        pass