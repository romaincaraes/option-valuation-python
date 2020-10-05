#!/usr/bin/env python
#coding: utf-8

import time, datetime
import numpy as np
import pandas as pd
import scipy.stats as sp
import models.binomial as bn
import models.blackscholes as bs
import models.montecarlo as mc

class Option() :
    def __init__(self, ul_asset, type, strike, expiry, style="EU") :
        self.type = type
        self.ul_asset = ul_asset
        self.strike = strike
        self.expiry = expiry
        self.style = style

    def days_to_expiry(self) :
        today = datetime.datetime.now()
        expiry = datetime.datetime.strptime(self.expiry, "%Y-%m-%d")
        days_to_expiry = (expiry - today).days
        return days_to_expiry

    def get_payoff(self, spot) :
        if (self.type == "call") :
            payoff = np.maximum(0, spot - self.strike)
        elif (self.type == "put") :
            payoff = np.maximum(0, self.strike - spot)
        return payoff
    
    def get_price(self, model, spot, riskfree, dividend, volatility) :
        price = {
            1 : bn.price(self, spot, riskfree, dividend, volatility),
            2 : bs.price(self, spot, riskfree, dividend, volatility),
            3 : mc.price(self, spot, riskfree, dividend, volatility)
        }.get(model)
        return price

    def snpdf(self, spot, riskfree, dividend, volatility) :
        snpdf = (1 / (np.sqrt(2 * np.pi))) * (np.exp((-bs.d1(self, spot, riskfree, dividend, volatility) ** 2) / 2))
        return snpdf

    def get_delta(self, spot, riskfree, dividend, volatility) :
        cdf = sp.norm(0, 1).cdf
        t = self.days_to_expiry()/365
        if (self.type == "call") :
            delta =  np.exp(-dividend * t) * cdf(bs.d1(self, spot, riskfree, dividend, volatility))
        elif (self.type == "put") :
            delta = np.exp(-dividend * t) * (cdf(bs.d1(self, spot, riskfree, dividend, volatility)) - 1)
        return delta

    def get_gamma(self, spot, riskfree, dividend, volatility) :
        t = self.days_to_expiry()/365
        gamma = (np.exp(-dividend * t) / (spot * volatility * np.sqrt(t))) * self.snpdf(spot, riskfree, dividend, volatility)
        return gamma

    def get_vega(self, spot, riskfree, dividend, volatility) :
        t = self.days_to_expiry()/365
        vega =  (0.01 * spot * np.exp(-dividend * t) * np.sqrt(t)) * self.snpdf(spot, riskfree, dividend, volatility)
        return vega

    def get_theta(self, spot, riskfree, dividend, volatility) :
        cdf = sp.norm(0, 1).cdf
        t = self.days_to_expiry()/365
        if (self.type == "call") :
            theta = (-(((spot * volatility * np.exp(-dividend * t)) / (2 * np.sqrt(t))) * self.snpdf(spot, riskfree, dividend, volatility)) - (riskfree * self.strike * np.exp(-riskfree * t) * cdf(bs.d2(self, spot, riskfree, dividend, volatility))) + (dividend * spot * np.exp(-dividend * t) * cdf(bs.d1(self, spot, riskfree, dividend, volatility))))/365
        elif (self.type == "put") :
            theta = (-(((spot * volatility * np.exp(-dividend * t)) / (2 * np.sqrt(t))) * self.snpdf(spot, riskfree, dividend, volatility)) + (riskfree * self.strike * np.exp(-riskfree * t) * cdf(-bs.d2(self, spot, riskfree, dividend, volatility))) - (dividend * spot * np.exp(-dividend * t) * cdf(-bs.d1(self, spot, riskfree, dividend, volatility))))/365
        return theta

    def get_rho(self, spot, riskfree, dividend, volatility) :
        cdf = sp.norm(0, 1).cdf
        t = self.days_to_expiry()/365
        if (self.type == "call") :
            rho = 0.01 * self.strike * t * np.exp(-riskfree * t) * cdf(bs.d2(self, spot, riskfree, dividend, volatility))
        elif (self.type == "put") :
            rho = -0.01 * self.strike * t * np.exp(-riskfree * t) * cdf(-bs.d2(self, spot, riskfree, dividend, volatility))
        return rho

    def get_greeks(self, spot, riskfree, dividend, volatility) :
        greeks = {
            "delta" : self.get_delta(spot, riskfree, dividend, volatility),
            "gamma" : self.get_gamma(spot, riskfree, dividend, volatility),
            "vega" : self.get_vega(spot, riskfree, dividend, volatility),
            "theta" : self.get_theta(spot, riskfree, dividend, volatility),
            "rho" : self.get_rho(spot, riskfree, dividend, volatility)
        }
        return greeks

class Call(Option) :
    def __init__(self, ul_asset, strike, expiry, style) :
        Option.__init__(self, ul_asset, type, strike, expiry, style)
        self.type = "call"

class Put(Option) :
    def __init__(self, ul_asset, strike, expiry, style) :
        Option.__init__(self, ul_asset, type, strike, expiry, style)
        self.type = "put"
    
def main() :
    pass

if __name__ == "__main__" :
    main()
