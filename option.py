#!/usr/bin/env python
#coding: utf-8

import time, datetime
import numpy as np
import pandas as pd
import scipy.stats as sp

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

    def d1(self, spot, riskfree, dividend, volatility) :
        t = self.days_to_expiry()/365
        d1 = (np.log(spot/self.strike) + ((riskfree - dividend) + 0.5 * volatility ** 2) * t) / (volatility * np.sqrt(t))
        return d1

    def d2(self, spot, riskfree, dividend, volatility) :
        t = self.days_to_expiry()/365
        d2 = self.d1(spot, riskfree, dividend, volatility) - volatility * np.sqrt(t)
        return d2

    def get_value(self, spot, riskfree, dividend, volatility) :
        cdf = sp.norm(0, 1).cdf
        t = self.days_to_expiry()/365
        if (self.type == "call") :
            value = spot * np.exp(-dividend * t) * cdf(self.d1(spot, riskfree, dividend, volatility)) - self.strike * np.exp(-riskfree * t) * cdf(self.d2(spot, riskfree, dividend, volatility))
        elif (self.type == "put") :
            value = np.exp(-riskfree * t) * self.strike * cdf(-self.d2(spot, riskfree, dividend, volatility)) - spot * np.exp(-dividend * t) * cdf(-self.d1(spot, riskfree, dividend, volatility))
        return value

    def snpdf(self, spot, riskfree, dividend, volatility) :
        snpdf = (1 / (np.sqrt(2 * np.pi))) * (np.exp((-self.d1(spot, riskfree, dividend, volatility) ** 2) / 2))
        return snpdf

    def get_delta(self, spot, riskfree, dividend, volatility) :
        cdf = sp.norm(0, 1).cdf
        t = self.days_to_expiry()/365
        if (self.type == "call") :
            delta =  np.exp(-dividend * t) * cdf(self.d1(spot, riskfree, dividend, volatility))
        elif (self.type == "put") :
            delta = np.exp(-dividend * t) * (cdf(self.d1(spot, riskfree, dividend, volatility)) - 1)
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
            theta = (-(((spot * volatility * np.exp(-dividend * t)) / (2 * np.sqrt(t))) * self.snpdf(spot, riskfree, dividend, volatility)) - (riskfree * self.strike * np.exp(-riskfree * t) * cdf(self.d2(spot, riskfree, dividend, volatility))) + (dividend * spot * np.exp(-dividend * t) * cdf(self.d1(spot, riskfree, dividend, volatility))))/365
        elif (self.type == "put") :
            theta = (-(((spot * volatility * np.exp(-dividend * t)) / (2 * np.sqrt(t))) * self.snpdf(spot, riskfree, dividend, volatility)) + (riskfree * self.strike * np.exp(-riskfree * t) * cdf(-self.d2(spot, riskfree, dividend, volatility))) - (dividend * spot * np.exp(-dividend * t) * cdf(-self.d1(spot, riskfree, dividend, volatility))))/365
        return theta

    def get_rho(self, spot, riskfree, dividend, volatility) :
        cdf = sp.norm(0, 1).cdf
        t = self.days_to_expiry()/365
        if (self.type == "call") :
            rho = 0.01 * self.strike * t * np.exp(-riskfree * t) * cdf(self.d2(spot, riskfree, dividend, volatility))
        elif (self.type == "put") :
            rho = -0.01 * self.strike * t * np.exp(-riskfree * t) * cdf(-self.d2(spot, riskfree, dividend, volatility))
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

def main() :
    pass

if __name__ == "__main__" :
    main()
