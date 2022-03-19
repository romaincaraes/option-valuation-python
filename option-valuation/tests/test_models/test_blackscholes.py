# test_blackscholes.py

from option import *
import models.blackscholes as bs

def test_blackscholes_d1(call, put, spot, riskfree, dividend, volatility):
    assert bs.d1(call, spot, riskfree, dividend, volatility)
    assert bs.d1(put, spot, riskfree, dividend, volatility)

def test_blackscholes_d2(call, put, spot, riskfree, dividend, volatility):
    assert bs.d2(call, spot, riskfree, dividend, volatility)
    assert bs.d2(put, spot, riskfree, dividend, volatility)
