#!/usr/bin/env python
#coding: utf-8

import numpy as np

def up(volatility, duration) :
    u = np.exp(volatility * np.sqrt(duration))
    return u
    
def down(volatility, duration) :
    d = np.exp(-volatility * np.sqrt(duration))
    return d
    
def tree(nodes) :
    return

def price(option, spot, riskfree, dividend, volatility) :
    return 0

def main() :
    pass

if __name__ == "__main__" :
    main()
