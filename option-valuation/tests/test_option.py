# test_option.py

from option import *

def test_option():
    o = Option("INDEX", "call", 100., "2021-12-31", "EU")
    assert True

def test_option_call():
    c = Call("INDEX", 100., "2021-12-31", "EU")
    assert True

def test_option_put():
    p = Put("INDEX", 100., "2021-12-31", "EU")
    assert True
