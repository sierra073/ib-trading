from ibapi.client import Contract
from market_reader import MarketReader
from datetime import datetime, timedelta
import time
import pandas as pd
from sqlalchemy import create_engine
import os

DATABASE_URL = os.environ.get('DATABASE_URL')

def get_earliest_date(client, contract):
    client.reqHeadTimeStamp(4101, contract, 'TRADES', 0, 1)
    time.sleep(2)

def get_historical_30s_data(client, contract):
    d = datetime.now()
    earliest_date = datetime.strptime(client.earliest_date, "%Y%m%d %H:%M:%S")
    delta = d - earliest_date
    number_of_days = delta.days
    print('number_of_days: ', number_of_days)

    for i in range(number_of_days):
        request_30s_data_1day(client, contract, d, i)
        d = d - timedelta(days=1)

    if (client.index >= (number_of_days - 1)):
        result = pd.DataFrame.from_records(client.data)
        print('data dimensions:', result.shape)
        insert_historical_data(result, contract.symbol)

def request_30s_data_1day(client, contract, d, i):
    endDateTime = d.strftime("%Y%m%d %H:%M:%S")
    print(i, ': requesting for ', endDateTime)
    client.reqHistoricalData(i, contract, endDateTime, '1 D', '30 secs', 'TRADES', 1, 1, False, [])
    time.sleep(5)

def insert_historical_data(result, ticker):
    engine = create_engine(DATABASE_URL)
    result.to_sql('historical_data_' + ticker.lower(), con=engine, if_exists='append', chunksize=1000, index=False)
    print('inserted data for ' + ticker)


def main():

    # Create the client and connect to TWS
    client = MarketReader('127.0.0.1', 4002, 0)

    contract = Contract()
    contract.symbol = 'SPY'
    contract.secType = 'STK'
    contract.exchange = 'SMART'
    contract.currency = 'USD'

    get_earliest_date(client, contract)
    get_historical_30s_data(client, contract)

    # Disconnect from TWS
    client.disconnect()

if __name__ == '__main__':
    main()