# test_option.py

from option import *

def test_option(option):
    assert isinstance(option, Option)

def test_option_call(call, spot, riskfree, dividend, volatility):
    assert isinstance(call.days_to_expiry(), int)
    assert isinstance(call.get_payoff(spot), float)
    assert isinstance(call.get_delta(spot, riskfree, dividend, volatility), float)

def test_option_put(put, spot, riskfree, dividend, volatility):
    assert isinstance(put.days_to_expiry(), int)
    assert isinstance(put.get_payoff(spot), float)
    assert isinstance(put.get_delta(spot, riskfree, dividend, volatility), float)
