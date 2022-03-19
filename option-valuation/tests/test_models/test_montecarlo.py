# test_montecarlo.py

from option import *
import models.montecarlo as mc

def test_montecarlo_price(call, put, spot, riskfree, dividend, volatility, steps, simulations):
    assert mc.price(call, spot, riskfree, dividend, volatility, steps, simulations)
    assert mc.price(put, spot, riskfree, dividend, volatility, steps, simulations)
