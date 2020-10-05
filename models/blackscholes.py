#!/usr/bin/env python
#coding: utf-8

import numpy as np
import scipy.stats as sp

def d1(option, spot, riskfree, dividend, volatility) :
    t = option.days_to_expiry()/365
    d1 = (np.log(spot/option.strike) + ((riskfree - dividend) + 0.5 * volatility ** 2) * t) / (volatility * np.sqrt(t))
    return d1

def d2(option, spot, riskfree, dividend, volatility) :
    t = option.days_to_expiry()/365
    d2 = d1(option, spot, riskfree, dividend, volatility) - volatility * np.sqrt(t)
    return d2

def price(option, spot, riskfree, dividend, volatility) :
    cdf = sp.norm(0, 1).cdf
    t = option.days_to_expiry()/365
    if (option.type == "call") :
        price = spot * np.exp(-dividend * t) * cdf(d1(option, spot, riskfree, dividend, volatility)) - option.strike * np.exp(-riskfree * t) * cdf(d2(option, spot, riskfree, dividend, volatility))
    elif (option.type == "put") :
        price = np.exp(-riskfree * t) * option.strike * cdf(-d2(option, spot, riskfree, dividend, volatility)) - spot * np.exp(-dividend * t) * cdf(-d1(option, spot, riskfree, dividend, volatility))
    return price

def main() :
    pass

if __name__ == "__main__" :
    main()
