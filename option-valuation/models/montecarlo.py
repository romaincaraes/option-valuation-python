#!/usr/bin/env python
#coding: utf-8

import numpy as np
import scipy.stats as sp

def price(option, spot, riskfree, dividend, volatility, steps=100, simulations=100000) :
    T = 1.
    dt = T / steps

    S = spot * np.exp(np.cumsum((riskfree - 0.5 * volatility ** 2) * dt + volatility * np.sqrt(dt) * np.random.standard_normal((steps + 1, simulations)), axis=0))

    S[0] = spot

    price = np.exp(-riskfree * T) * np.sum(np.maximum(S[-1] - option.strike, 0)) / simulations

    return price

def main() :
    pass

if __name__ == "__main__" :
    main()
