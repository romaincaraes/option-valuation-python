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
    q = 1 - p

    ul_price = np.zeros([steps + 1, steps + 1])
    ul_price[0, 0] = spot
    for i in range(1, steps + 1) :
        ul_price[i, 0] = ul_price[i - 1, 0] * u
        for j in range(1, i + 1) :
            ul_price[i, j] = ul_price[i - 1, j - 1] * d

    option_price = np.zeros([steps + 1, steps + 1])
    for j in range(steps + 1) :
        if option.type == "call" :
            option_price[steps, j] = max(0, ul_price[steps, j] - option.strike)
        elif option.type == "put" :
            option_price[steps, j] = max(0, option.strike - ul_price[steps, j])

    for i in range(steps)[::-1] :
        for j in range(i + 1) :
            if option.style == "EU" :
                option_price[i, j] = np.exp(-riskfree * dt) * (p * option_price[i + 1, j] + q * option_price[i + 1, j + 1])
            elif option.style == "US" :
                if option.type == "call" :
                    option_price[i, j] = max(ul_price[i, j] - option.strike, np.exp(-riskfree * dt) * (p * option_price[i + 1, j] + q * option_price[i + 1, j + 1])) 
                elif option.type == "put" :
                    option_price[i, j] = max(option.strike - ul_price[i, j], np.exp(-riskfree * dt) * (p * option_price[i + 1, j] + q * option_price[i + 1, j + 1]))

    return option_price[0, 0]

def main() :
    pass

if __name__ == "__main__" :
    main()
