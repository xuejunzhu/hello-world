# -*- coding: utf-8 -*-
"""
Created on Sun Nov 15 01:05:37 2020
https://medium.com/@kannansi/how-to-price-barrier-option-using-quantlib-python-ee4b1fff2448
https://github.com/kannansingaravelu/QuantLib-Python/blob/master/BarrierOption.ipynb
@author: junz
"""

# Import required library
from QuantLib import *

'''
The Barrier Option
A Barrier Option is a derivative whose payoff depends on whether the price of the underlying security crosses a pre specified level (called the ‘barrier’) before the expiration.
In [2]:
'''

# Barrier Option: Up-and-Out Call 
# Strike 100, Barrier 150, Rebate 50, Exercise date 4 years 

#Set up the global evaluation date to today
today = Date(28,February,2020)
Settings.instance().evaluationDate = today

# Specify option
option = BarrierOption(Barrier.UpOut, 150.0, 50.0, 
                       PlainVanillaPayoff(Option.Call, 100.0), 
                       EuropeanExercise(Date(29, February, 2024)))

'''
We will now pass the market data: spot price : 100, risk-free rate: 1% and sigma: 30%
In [3]:
    '''

# Underlying Price
u = SimpleQuote(100)
# Risk-free Rate
r = SimpleQuote(0.01)
# Sigma 
sigma = SimpleQuote(0.30)

# Build flat curves and volatility
riskFreeCurve = FlatForward(0, TARGET(), QuoteHandle(r), Actual360())
volatility = BlackConstantVol(0, TARGET(), QuoteHandle(sigma), Actual360())

'''
Model and Pricing Engine
Build the pricing engine by encapsulating the market data in a Black-Scholes process
In [4]:
'''

# Stochastic Process
process = BlackScholesProcess(QuoteHandle(u), 
                              YieldTermStructureHandle(riskFreeCurve), 
                              BlackVolTermStructureHandle(volatility))

# Build the engine (based on an analytic formula) and set it to the option for evaluation
option.setPricingEngine(AnalyticBarrierEngine(process))

'''
Market Data Changes
Change the market data to get new option pricing.
In [5]:
'''

# Set initial value and define h
u0 = u.value(); h=0.01
P0 = option.NPV()

# Bump up the price by h
u.setValue(u0+h)
P_plus = option.NPV()

# Bump down the price by h
u.setValue(u0-h)
P_minus = option.NPV() 

# Set the price back to its current value
u.setValue(u0)

'''
Calculation of Greeks
In [6]:
'''

# Calculate Greeks: Delta, Gamma, Vega, Theta, Rho
delta = (P_plus - P_minus)/(2*h)
gamma = (P_plus - 2*P0 + P_minus)/(h*h)

# Update quote for rho calculation
r0 = r.value(); h1 = 0.0001
r.setValue(r0+h); P_plus = option.NPV()
r.setValue(r0)

# Rho
rho = (P_plus - P0)/h1

# Update quote for sigma calculation
sigma0 = sigma.value() ; h = 0.0001
sigma.setValue(sigma0+h) ; P_plus = option.NPV()
sigma.setValue(sigma0)

# Vega
vega = (P_plus - P0)/h

# Update quote to calculate theta
#Settings.instance().evaluationDate = today+1
P1 = option.NPV()
h = 1.0/365

# Theta
theta = (P1-P0)/h


print(f'OptionPrice: {P0: .2f}, Delta: {delta: .2f}, Gamma: {gamma: .4f}, Theta: {theta: .2f}, Vega: {vega: .2f}, Rho: {rho: .2f}')

'''
OptionPrice:  22.06, Delta:  0.52, Gamma:  0.0032, Theta: -5.25, Vega:  41.75, Rho:  7248.60
Derivatives pricing using QuantLib-Python is part of 'Python For Derivatives' module. For further details, refer http://kannansingaravelu.com

'''