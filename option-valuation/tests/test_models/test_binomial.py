# test_binomial.py

from option import *
import models.binomial as bn

def test_binomial_up(volatility, steps):
    assert bn.up(volatility, 60/(365*steps))