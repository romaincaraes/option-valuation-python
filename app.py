#!/usr/bin/env python
#coding: utf-8

import datetime
import option
import pandas as pd
import streamlit as st

model = st.sidebar.selectbox("Model", ["Black & Scholes"])

def user_input_features() :
    st.sidebar.header("Option")
    type = st.sidebar.selectbox("Type", ["Call", "Put"])
    ul_asset = st.sidebar.text_input("Underlying Asset", "EURUSD")
    spot = st.sidebar.number_input("Spot", 0.0000, 2.0000, 1.1850, step=0.0005, format="%.4f")
    strike = st.sidebar.number_input("Strike", 0.0000, 2.0000, 1.1650, step=0.0005, format="%.4f")
    expiry = st.sidebar.date_input("Expiry", datetime.date(2020, 12, 31))
    style = st.sidebar.selectbox("Style", ["EU"])
    
    st.sidebar.header("Market")
    riskfree = st.sidebar.slider("Riskfree Rate", 0.00, 10.00, 1.00, step=0.05)
    volatility = st.sidebar.slider("Implied Volatility", 0.00, 1.00, 0.20, step=0.01)

    data = {
        "type" : type.lower(),
        "ul_asset" : ul_asset,
        "strike" : strike,
        "spot" : spot,
        "expiry" : expiry.strftime("%Y-%m-%d"),
        "style" : style,
        "riskfree" : riskfree,
        "volatility" : volatility
    }
    features = pd.DataFrame(data, index=[0])
    return features

st.subheader("User Input Parameters")    
features = user_input_features()
st.write(features)

spot = features['spot'][0]
riskfree = features['riskfree'][0]
volatility = features['volatility'][0]

option = option.Option(
    ul_asset=features['ul_asset'][0],
    type=features['type'][0],
    strike=features['strike'][0],
    expiry=features['expiry'][0],
    style=features['style'][0]
)

st.subheader("Output")
payoff = {"payoff" : float(option.get_payoff(spot))}
value = {"value" : float(option.get_value(spot, riskfree, 0.0, volatility))}
greeks = option.get_greeks(spot, riskfree, 0.0, volatility)
output = {**payoff, **value, **greeks}
df = pd.DataFrame(output, index=[0])
st.write(df)
