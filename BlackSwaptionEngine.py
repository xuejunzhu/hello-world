# -*- coding: utf-8 -*-
"""
Created on Fri Nov 13 16:51:55 2020
https://github.com/lballabio/QuantLib-SWIG/issues/98
@author: junz
"""

# choose either shifted lognormal or normal model
# http://quantlib.org/slides/qlum15/caspers1.pdf

# displacement = 0.1
# voltype = ql.ShiftedLognormal

import math
from collections import namedtuple

def create_swaption_helpers(data, index, term_structure, engine):
    '''Implement function missing from guide
    '''
    # based on
    # http://khandrikacm.blogspot.ch/2014/03/european-style-interest-rate-swaption.html
    swaptions = [ql.SwaptionHelper(ql.Period(swap.start, ql.Years),
                                   ql.Period(swap.length, ql.Years),
                                   ql.QuoteHandle(ql.SimpleQuote(swap.volatility)),
                                   index, index.tenor(),
                                   index.dayCounter(), index.dayCounter(),
                                   term_structure) for swap in data]
    for swap in swaptions:
        swap.setPricingEngine(engine)
    return swaptions



'''
def create_swaption_helpers(data, index, term_structure, engine):
    swaptions = []
    fixed_leg_tenor = ql.Period(1, ql.Years)
    fixed_leg_daycounter = ql.Actual360()
    floating_leg_daycounter = ql.Actual360()
    for d in data:
        vol_handle = ql.QuoteHandle(ql.SimpleQuote(d.volatility))
        helper = ql.SwaptionHelper(ql.Period(d.start, ql.Years),
                                   ql.Period(d.length, ql.Years),
                                   vol_handle,
                                   index,
                                   fixed_leg_tenor,
                                   fixed_leg_daycounter,
                                   floating_leg_daycounter,
                                   term_structure,
                                   ql.CalibrationHelper.RelativePriceError,
                                   ql.nullDouble(),
                                   1.,
                                   ql.Normal,
                                   0.
                                   )
        helper.setPricingEngine(engine)
        swaptions.append(helper)
    return swaptions  
'''

def calibration_report(swaptions, data):
    print ("-"*82)
    print ("%15s %15s %15s %15s %15s" % \
    ("Model Price", "Market Price", "Implied Vol", "Market Vol", "Rel Error"))
    print ("-"*82)
    cum_err = 0.0
    for i, s in enumerate(swaptions):
        model_price = s.modelValue()
        market_vol = data[i].volatility
        black_price = s.blackPrice(market_vol)
        rel_error = model_price/black_price - 1.0
        implied_vol = s.impliedVolatility(model_price,
                                          1e-5, 50, 0.0, 0.50)
        rel_error2 = implied_vol/market_vol-1.0
        cum_err += rel_error2*rel_error2
        
        print ("%15.5f %15.5f %15.5f %15.5f %15.5f" % \
        (model_price, black_price, implied_vol, market_vol, rel_error))
    print ("-"*82)
    print ("Cumulative Error : %15.5f" % math.sqrt(cum_err))
    

today = ql.Date(15, ql.February, 2002);
settlement= ql.Date(19, ql.February, 2002);
ql.Settings.instance().evaluationDate = today;
term_structure = ql.YieldTermStructureHandle(
    ql.FlatForward(settlement, 0.04875825, ql.Actual365Fixed())
    )
index = ql.Euribor1Y(term_structure)
CalibrationData = namedtuple("CalibrationData", 
                             "start, length, volatility")
data = [CalibrationData(1, 5, 0.1148),
        CalibrationData(2, 4, 0.1108),
        CalibrationData(3, 3, 0.1070),
        CalibrationData(4, 2, 0.1021),
        CalibrationData(5, 1, 0.1000 )]
model = ql.HullWhite(term_structure);
engine = ql.JamshidianSwaptionEngine(model)
swaptions = create_swaption_helpers(data, index, term_structure, engine)

optimization_method = ql.LevenbergMarquardt(1.0e-8,1.0e-8,1.0e-8)
end_criteria = ql.EndCriteria(10000, 100, 1e-6, 1e-8, 1e-8)
model.calibrate(swaptions, optimization_method, end_criteria)

a, sigma = model.params()
print ("a = %6.5f, sigma = %6.5f" % (a, sigma))
