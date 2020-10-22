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
    dt = (option.days_to_expiry()/365) / 4
    return 0

def main() :
    pass

if __name__ == "__main__" :
    main()
