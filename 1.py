'''
(c) 2011, 2012 Georgia Tech Research Corporation
This source code is released under the New BSD license.  Please see
http://wiki.quantsoftware.org/index.php?title=QSTK_License
for license details.

Created on January, 24, 2013

@author: Sourabh Bajaj
@contact: sourabhbajaj@gatech.edu
@summary: Example tutorial code.
'''

# QSTK Imports
import QSTK.qstkutil.qsdateutil as du
import QSTK.qstkutil.tsutil as tsu
import QSTK.qstkutil.DataAccess as da

# Third Party Imports
import datetime as dt
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

def simulate(startdate, enddate, sym_list, alloc_list, closing_price):
   
    # Get closing prices
    closing_price = closing_price
    
    # normalize
    normalized_closing_price = closing_price / closing_price[0, :]
    
    # make a copy
    na_rets = normalized_closing_price.copy()    

    daily_returns = np.sum(na_rets * alloc_list, axis=1)
    tsu.returnize0(daily_returns)

    averageReturn = np.mean(daily_returns)
    

    stDev = np.std(daily_returns)
    

    cumulativeReturns = np.cumprod(daily_returns + 1)
    cumulativeReturn = cumulativeReturns[-1:][-1:]
    

    k = np.sqrt(252)

    sharpeRatio = (averageReturn / stDev) * k;

    return (stDev, averageReturn, sharpeRatio, cumulativeReturn);

def main():
    ''' Main Function'''

    ls_port_syms = ['BRCM', 'TXN', 'AMD', 'ADI']

    # Reading the historical data.
    dt_start = dt.datetime(2011, 1, 1)
    dt_end = dt.datetime(2011, 12, 31)

    # Creating an object of the dataaccess class with Yahoo as the source.
    c_dataobj = da.DataAccess('Yahoo', cachestalltime=0)
        
    # We need closing prices so the timestamp should be hours=16.
    dt_timeofday = dt.timedelta(hours=16)

    # Get a list of trading days between the start and the end.
    ldt_timestamps = du.getNYSEdays(dt_start, dt_end, dt_timeofday)

    # Keys to be read from the data, it is good to read everything in one go.
    ls_keys = ['open', 'high', 'low', 'close', 'volume', 'actual_close']

    # Reading the data, now d_data is a dictionary with the keys above.
    # Timestamps and symbols are the ones that were specified before.
    ldf_data = c_dataobj.get_data(ldt_timestamps, ls_port_syms, ls_keys)
    d_data = dict(zip(ls_keys, ldf_data))

    closing_price = d_data['close'].values
    
    maxSharpRatio = 0.0
    maxVol = 0.0
    maxDaily_ret = 0.0
    maxCum_ret = 0.0
    loopValues = np.arange(0,1.1,0.1)
    f =0.0
    s = 0.0
    t = 0.0
    fo = 0.0
    for first in loopValues:
        for second in loopValues:
            for third in loopValues:
                for fourth in loopValues:
                    okSum = first + second + third + fourth
                    if (okSum == 1.0):
                        lf_port_alloc = [first, second, third, fourth]
                        vol, daily_ret, sharpe, cum_ret = simulate(dt_start, dt_end, ls_port_syms, lf_port_alloc, closing_price)
                        if (sharpe > maxSharpRatio):
                            maxSharpRatio = sharpe;
                            maxVol = vol;
                            maxDaily_ret = daily_ret;
                            maxCum_ret = cum_ret;
                            f = first
                            s = second
                            t = third
                            fo = fourth

    averageReturnString = 'Average Daily Return: %f' % (maxDaily_ret,)
    stDevString = 'Volatility (stdev of daily returns): %f' % (maxVol,)
    cumulativeReturnString = 'Cumulative Return: %f' % (cum_ret,)    
    sharpeRatioString = 'Sharpe Ratio: %f' % (maxSharpRatio,)
    
    print 'Start Date: ', dt_start
    print 'End Date: ', dt_end
    print sharpeRatioString
    print stDevString
    print averageReturnString
    print cumulativeReturnString
    print '%d %d %d %d' % (f,s,t,fo)
                            
                            
if __name__ == '__main__':
    main()





