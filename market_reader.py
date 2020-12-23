''' Demonstrates different ways to request financial data '''
from threading import Thread
import pandas as pd
import time

from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.utils import iswrapper

class MarketReader(EWrapper, EClient):
    ''' Serves as the client and the wrapper for requesting historical bar data for a single ticker'''

    def __init__(self, addr, port, client_id):
        EClient. __init__(self, self)
        self.index = 0
        self.data = []
        self.earliest_date = ''

        # Connect to TWS
        self.connect(addr, port, client_id)

        # Launch the client thread
        thread = Thread(target=self.run)
        thread.start()

    @iswrapper
    def historicalData(self, req_id, bar):
        ''' Called in response to reqHistoricalData '''
        bar_dict = {
            'time': bar.date,
            'open': bar.open,
            'high': bar.high,
            'low': bar.low,
            'close': bar.close,
            'avg': bar.average,
            'volume': bar.volume
        }
        self.data.append(bar_dict)

    @iswrapper
    def historicalDataEnd(self, req_id, start, end):
        ''' Called after historical data has been received '''
        self.index += 1

    @iswrapper
    def headTimestamp(self, req_id, headTimestamp):
        print("HeadTimeStamp: ", headTimestamp)
        self.earliest_date = headTimestamp

    @iswrapper
    def error(self, req_id, code, msg):
        ''' Called if an error occurs '''

        print('Error {} for request {}: {}'.format(code, req_id, msg))