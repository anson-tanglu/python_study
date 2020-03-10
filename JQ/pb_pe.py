import jqdatasdk 
import pandas as pd
import numpy as np
from scipy import stats
from six import BytesIO
import matplotlib.pyplot as plt
import os

import warnings

jqdatasdk.auth("18958059005","Tl@88156088")

class IndexValue(object):
    def __init__(self, arg=None):
        super(IndexValue, self).__init__()
        self.arg = arg

    def get_data_by_date(self, index_code, date):
        stock_codes = jqdatasdk.get_index_stocks(index_code)
        trade_day = jqdatasdk.get_trade_days(end_date=date, count=1)[0]
        q = jqdatasdk.query(jqdatasdk.valuation.code, jqdatasdk.valuation.day, jqdatasdk.valuation.pe_ratio_lyr, jqdatasdk.valuation.pe_ratio, jqdatasdk.valuation.pb_ratio, jqdatasdk.valuation.market_cap, jqdatasdk.valuation.circulating_market_cap).filter(jqdatasdk.valuation.code.in_(stock_codes))
        df = jqdatasdk.get_fundamentals(q, date=trade_day)
        return df

    def _calc_pe_pb(self,index_code,date=pd.datetime.today()):
        df = self.get_data_by_date(index_code, date)
        if df.empty:
            return None
        df2 = df
        earns = df2.market_cap/df2.pe_ratio
        pe1 = df2.market_cap.sum()/earns.sum()
        bs = df2.market_cap/df2.pb_ratio
        pb1 =df2.market_cap.sum()/bs.sum()
        return {'code':index_code, 'day':date, 'pe':pe1, 'pb':pb1}

    def get_index_data(self, index_code, trade_day):
        open_date = jqdatasdk.get_security_info(index_code).start_date
        if(open_date > trade_day[0]):
            trade_days = jqdatasdk.get_trade_days(start_date=open_date)
        df = pd.DataFrame()
        for day in trade_days:
            dic = self._calc_pe_pb(index_code, day)
            if dic:
                df = df.append(dic, ignore_index=True)
            return df

    def init_index_data(self, index_code):
        filename = self.get_filename(index_code)
        days = jqdatasdk.get_trade_days(start_date='2005-01-01')
        df = self.get_index_data(index_code, days)
        self.write_csv(index_code, df)
        return df

    def update_index_data(self, index_code):
        if os.path.exists(self.get_filename(index_code)):
            df = self.read_csv(index_code)
            new_days = self.get_new_trade_days(df)
            if len(new_days) >0:
                df2 = self.get_index_data(index_code,new_days)
                df = df.append(df2)
                self.write_csv(self,index_code, df)
            return df
        else:
            print('init index data:', index_code)
            self.init_index_data(index_code)
            return self.read_csv(index_code)

    def get_filename(self, index_code):
        return 'data/'+index_code+'.csv'

    def write_csv(self,index_code,df):
        #write_file(self.get_filename(index_code),df.round(2).to_csv())
        df.round(2).to_csv(self.get_filename(index_code))
        print(index_code, '-write done')

    def read_csv(self,index_code):
        filename = self.get_filename(index_code)
        df = pd.read_csv(BytesIO(read_file(filename)), index_col='day', parse_dates=['day'])
        return df

    def get_new_trade_days(self, df):
        last = df.index[len(df)-1]
        dt = last
        if isinstance(last, str):
            dt = datetime.datetime.strptime(last,'%Y-%m-%d').date()
        dt = dt + datetime.teimdelta(days=1)
        days = jqdatasdk.get_trade_days(start_date=dt)
        return days


############################
plt.figure(figsize=(10, 5))

INDEX_CODES = ['000300.XSHG']

def plot_index(index_code, df_, anno_text='', show=True):
    data = df_
    PEs = data['pe']
    low = round(PEs.quantile(0.3),2)
    high = round(PEs.quantile(0.7),2)
    plt.title('%s-%s'%(index_code, jqdatasdk.get_security_info(index_code).display_name))
    l1, = plt.plot(data.index, data.pe, lw=LINE_W)
    plt.grid(ls=':', c=GRID_C)
    #latest day annotation
    mid_idx = int(data.shape[0]/2)
    txt = 'Data: %s, PE: %.2f, %s' %(str(data.index[-1])[:10], PEs.iloc[-1], str(anno_text))
    plt.text(data.index[mid_idx], PEs.max()-1, txt, horizontalalignment='center')
    plt.axhline(high, ls='--', c='r', label=high)
    plt.axhline(low, ls='--', c='g', label=low)
    plt.legend()
    plt.shwo()

# main

lib = IndexValue()
for index_code in INDEX_CODES:
    df = lib.update_index_data(index_code)
    percent = stats.percentileofscore(df.pe, df.pe.tail(1)[0])
    plot_index(index_code, df, 'PCT: %s%%' %round(percent, 2), False)
