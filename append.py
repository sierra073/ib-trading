from ibapi.client import Contract
from market_reader import MarketReader
from datetime import datetime, timedelta
import time
import pandas as pd

def main():

    # Create the client and connect to TWS
    client = MarketReader('127.0.0.1', 4002, 0)

    # Request the current time
    con = Contract()
    con.symbol = 'SPY'
    con.secType = 'STK'
    con.exchange = 'SMART'
    con.currency = 'USD'

    # Request historical bars
    d = datetime.now()

    for i in range(30):
        endDateTime = d.strftime("%Y%m%d %H:%M:%S")
        print(i, ': requesting for ', endDateTime)
        client.reqHistoricalData(i, con, endDateTime, '1 D', '30 secs', 'TRADES', 1, 1, False, [])
        d = d - timedelta(days=1)
        time.sleep(5)

    if (client.index >= 29):
        result = pd.DataFrame.from_records(client.data)
        print(result.shape)
        print(result.head())

    # Disconnect from TWS
    client.disconnect()

if __name__ == '__main__':
    main()