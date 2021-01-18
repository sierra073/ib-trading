from market_reader_historical import MarketReaderHistorical
from ibapi.client import Contract
import time
from datetime import datetime
from sqlalchemy import create_engine, Table, Column, Text, MetaData
import os

DATABASE_URL = os.environ.get('DATABASE_URL')
TICKER_LIST = os.environ.get('TICKER_LIST').split(',')
engine = create_engine(DATABASE_URL)
meta = MetaData(engine)

ticker_metadata  = Table(
    'ticker_metadata', meta, 
    Column('ticker', Text, primary_key = True), 
    Column('earliest_date', Text)
    )
meta.create_all()

def get_earliest_date_for_symbol(symbol, conn, **kwargs):
    client = MarketReaderHistorical('tws', 4004, 0)
    contract = Contract()
    contract.symbol = symbol
    contract.secType = kwargs.get('secType', 'STK')
    contract.exchange = kwargs.get('exchange', 'SMART')
    contract.currency = kwargs.get('currency', 'USD')
    print('connected and getting earliest date for ' + symbol)
    earliest_date = get_earliest_date(client, contract)

    if earliest_date is not None:
        earliest_date = datetime.strptime(earliest_date, "%Y%m%d %H:%M:%S")
        insert_earliest_date_for_symbol(symbol, earliest_date, conn)
    client.disconnect()

def get_earliest_date(client, contract):
    client.reqHeadTimeStamp(1, contract, 'TRADES', 0, 1)
    time.sleep(1)
    return client.earliest_date

def insert_earliest_date_for_symbol(symbol, earliest_date, conn):
    try:
        ins = ticker_metadata.insert().values(ticker=symbol, earliest_date=earliest_date)
        conn.execute(ins)
    except Exception:
        pass

def retrieve_earliest_date_for_symbol(symbol):
    select_st = ticker_metadata.select().where(
    ticker_metadata.c.ticker == symbol)
    res = conn.execute(select_st)
    for _row in res:
        return _row[1]

if __name__ == '__main__':
    conn = engine.connect()
    for symbol in TICKER_LIST:
        get_earliest_date_for_symbol(symbol, conn)

