# test_option.py

from option import *

def test_option():
    o = Option(ul_asset="INDEX", type="call", strike=100., expiry="2021-12-31", style="EU")
    assert True

def test_option_call():
    c = Call(ul_asset="INDEX", strike=100., expiry="2021-12-31", style="EU")
    assert True

def test_option_put():
    p = Put(ul_asset="INDEX", strike=100., expiry="2021-12-31", style="EU")
    assert True
