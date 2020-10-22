#!/usr/bin/env python
#coding: utf-8

import numpy as np

def up(volatility, duration) :
    u = np.exp(volatility * np.sqrt(duration))
    return u

def down(volatility, duration) :
    d = np.exp(-volatility * np.sqrt(duration))
    return d

def price(option, spot, riskfree, dividend, volatility) :
    steps = 4
    dt = option.days_to_expiry() / (365 * steps)

    u = up(volatility, dt)
    d = down(volatility, dt)

    p = (np.exp(riskfree * dt) - d) / (u - d)

    ul_price = np.zeros([steps + 1, steps + 1])
    ul_price[0, 0] = spot
    for i in range(1, steps + 1) :
        ul_price[i, 0] = ul_price[i - 1, 0] * u
        for j in range(1, i + 1) :
            ul_price[i, j] = ul_price[i - 1, j - 1] * d

    option_price = np.zeros([steps + 1, steps + 1])

    return option_price[0, 0]

def main() :
    pass

if __name__ == "__main__" :
    main()
