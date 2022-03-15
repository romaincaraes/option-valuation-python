#!/usr/bin/env python3
#coding: utf-8

import time, datetime
import numpy as np
import pandas as pd
import scipy.stats as sp
import streamlit as st
import models.binomial as bn
import models.blackscholes as bs
import models.montecarlo as mc

class Option():
    def __init__(self, ul_asset, type, strike, expiry, style="EU"):
        self.type = type
        self.ul_asset = ul_asset
        self.strike = strike
        self.expiry = expiry
        self.style = style

    def days_to_expiry(self):
        today = datetime.datetime.now()
        expiry = datetime.datetime.strptime(self.expiry, "%Y-%m-%d")
        days_to_expiry = (expiry - today).days
        return days_to_expiry

    def get_payoff(self, spot):
        if (self.type == "call"):
            payoff = np.maximum(0, spot - self.strike)
        elif (self.type == "put"):
            payoff = np.maximum(0, self.strike - spot)
        return payoff

    def get_price(self, model, **kwargs):
        if (model == 1):
            price = bn.price(self, spot=kwargs['spot'], riskfree=kwargs['riskfree'], dividend=kwargs['dividend'], volatility=kwargs['volatility'], steps=kwargs['steps'])
        elif (model == 2):
            price = bs.price(self, spot=kwargs['spot'], riskfree=kwargs['riskfree'], dividend=kwargs['dividend'], volatility=kwargs['volatility'])
        elif (model == 3): 
            price = mc.price(self, spot=kwargs['spot'], riskfree=kwargs['riskfree'], dividend=kwargs['dividend'], volatility=kwargs['volatility'], steps=kwargs['steps'], simulations=kwargs['simulations'])
        return price

    def snpdf(self, spot, riskfree, dividend, volatility):
        snpdf = (1 / (np.sqrt(2 * np.pi))) * (np.exp((-bs.d1(self, spot, riskfree, dividend, volatility) ** 2) / 2))
        return snpdf

    def get_delta(self, spot, riskfree, dividend, volatility):
        cdf = sp.norm(0, 1).cdf
        t = self.days_to_expiry() / 365
        if (self.type == "call"):
            delta = np.exp(-dividend * t) * cdf(bs.d1(self, spot, riskfree, dividend, volatility))
        elif (self.type == "put"):
            delta = np.exp(-dividend * t) * (cdf(bs.d1(self, spot, riskfree, dividend, volatility)) - 1)
        return delta

    def get_gamma(self, spot, riskfree, dividend, volatility):
        t = self.days_to_expiry() / 365
        gamma = (np.exp(-dividend * t) / (spot * volatility * np.sqrt(t))) * self.snpdf(spot, riskfree, dividend, volatility)
        return gamma

    def get_vega(self, spot, riskfree, dividend, volatility):
        t = self.days_to_expiry() / 365
        vega = (0.01 * spot * np.exp(-dividend * t) * np.sqrt(t)) * self.snpdf(spot, riskfree, dividend, volatility)
        return vega

    def get_theta(self, spot, riskfree, dividend, volatility):
        cdf = sp.norm(0, 1).cdf
        t = self.days_to_expiry() / 365
        if (self.type == "call"):
            theta = (-(((spot * volatility * np.exp(-dividend * t)) / (2 * np.sqrt(t))) * self.snpdf(spot, riskfree, dividend, volatility)) - (riskfree * self.strike * np.exp(-riskfree * t) * cdf(bs.d2(self, spot, riskfree, dividend, volatility))) + (dividend * spot * np.exp(-dividend * t) * cdf(bs.d1(self, spot, riskfree, dividend, volatility)))) / 365
        elif (self.type == "put"):
            theta = (-(((spot * volatility * np.exp(-dividend * t)) / (2 * np.sqrt(t))) * self.snpdf(spot, riskfree, dividend, volatility)) + (riskfree * self.strike * np.exp(-riskfree * t) * cdf(-bs.d2(self, spot, riskfree, dividend, volatility))) - (dividend * spot * np.exp(-dividend * t) * cdf(-bs.d1(self, spot, riskfree, dividend, volatility)))) / 365
        return theta

    def get_rho(self, spot, riskfree, dividend, volatility):
        cdf = sp.norm(0, 1).cdf
        t = self.days_to_expiry() / 365
        if (self.type == "call"):
            rho = 0.01 * self.strike * t * np.exp(-riskfree * t) * cdf(bs.d2(self, spot, riskfree, dividend, volatility))
        elif (self.type == "put"):
            rho = -0.01 * self.strike * t * np.exp(-riskfree * t) * cdf(-bs.d2(self, spot, riskfree, dividend, volatility))
        return rho

    def get_greeks(self, spot, riskfree, dividend, volatility):
        greeks = {
            "delta": self.get_delta(spot, riskfree, dividend, volatility),
            "gamma": self.get_gamma(spot, riskfree, dividend, volatility),
            "vega": self.get_vega(spot, riskfree, dividend, volatility),
            "theta": self.get_theta(spot, riskfree, dividend, volatility),
            "rho": self.get_rho(spot, riskfree, dividend, volatility)
        }
        return greeks

class Call(Option):
    def __init__(self, ul_asset, strike, expiry, style):
        Option.__init__(self, ul_asset, type, strike, expiry, style)
        self.type = "call"

class Put(Option):
    def __init__(self, ul_asset, strike, expiry, style):
        Option.__init__(self, ul_asset, type, strike, expiry, style)
        self.type = "put"

model = {1:"Binomial", 2:"Black & Scholes", 3:"Monte Carlo"}
model = st.sidebar.selectbox(label="Model", options=list(model.keys()), index=1, format_func=lambda x: model[x])

if (model == 1): # Binomial
    st.sidebar.header("Model Parameters")
    steps = st.sidebar.number_input(label="Steps", min_value=1, value=4)
    simulations = 0
elif (model == 2): # Black & Scholes
    steps = 0
    simulations = 0
elif (model == 3): # Monte Carlo
    st.sidebar.header("Model Parameters")
    steps = st.sidebar.number_input(label="Steps", min_value=1, value=100)
    simulations = st.sidebar.number_input(label="Simulations", min_value=1, max_value=100000, value=100000)

def user_input_features():
    st.sidebar.header("Option")
    type = st.sidebar.selectbox(label="Type", options=["Call", "Put"])
    ul_asset = st.sidebar.text_input(label="Underlying Asset", value="EURUSD")
    spot = st.sidebar.number_input(label="Spot", min_value=0.0, value=1.1850, step=0.0005, format="%.4f")
    strike = st.sidebar.number_input(label="Strike", min_value=0.0, value=1.1650, step=0.0005, format="%.4f")
    expiry = st.sidebar.date_input(label="Expiry", value=datetime.date(2021, 12, 31))
    style = st.sidebar.selectbox(label="Style", options=["EU", "US"], index=0)

    st.sidebar.header("Market")
    riskfree = st.sidebar.slider(label="Riskfree Rate", min_value=0.0, max_value=1.0, value=.05, step=0.01)
    dividend = st.sidebar.number_input(label="Dividend", min_value=0.0, value=0.0)
    volatility = st.sidebar.slider(label="Implied Volatility", min_value=0.0, max_value=1.0, value=0.2, step=0.0005)

    data = {
        "type": type.lower(),
        "ul_asset": ul_asset,
        "strike": strike,
        "spot": spot,
        "expiry": expiry.strftime("%Y-%m-%d"),
        "style": style,
        "riskfree": riskfree,
        "dividend": dividend,
        "volatility": volatility
    }
    features = pd.DataFrame(data, index=[0])
    return features

st.header("User Input Parameters")
st.subheader("Option")
features = user_input_features()
st.write(features[['type', 'ul_asset', 'strike', 'spot', 'expiry', 'style']])
st.subheader("Market")
st.write(features[['riskfree', 'dividend', 'volatility']])

spot = features['spot'][0]
riskfree = features['riskfree'][0]
dividend = features['dividend'][0]
volatility = features['volatility'][0]

option = Option(
    ul_asset=features['ul_asset'][0],
    type=features['type'][0],
    strike=features['strike'][0],
    expiry=features['expiry'][0],
    style=features['style'][0]
)

st.header("Output")
payoff = {"payoff": float(option.get_payoff(spot=spot))}
price = {"price": float(option.get_price(model=model, spot=spot, riskfree=riskfree, dividend=dividend, volatility=volatility, steps=steps, simulations=simulations))}
greeks = option.get_greeks(spot=spot, riskfree=riskfree, dividend=dividend, volatility=volatility)
output = {**payoff, **price, **greeks}
df = pd.DataFrame(output, index=[0])
st.write(df)

def main():
    pass

if __name__ == "__main__":
    main()
