import pytest
import random
import datetime
from option import *

@pytest.fixture
def option():
    option = Option(
        ul_asset="UL_ASSET",
        type=lambda t : "call" if (t > 0.5) else "put",
        strike=random.randint(0,10e12),
        expiry=(datetime.datetime.now() + datetime.timedelta(days=random.randint(0,36500))).strftime("%Y-%m-%d"),
        style="EU"
    )
    return option

@pytest.fixture
def call():
    call = Call(
        ul_asset="UL_ASSET",
        strike=random.randint(0,10e12),
        expiry=(datetime.datetime.now() + datetime.timedelta(days=random.randint(0,36500))).strftime("%Y-%m-%d"),
        style="EU"
    )
    return call

@pytest.fixture
def put():
    put = Put(
        ul_asset="UL_ASSET",
        strike=random.randint(0,10e12),
        expiry=(datetime.datetime.now() + datetime.timedelta(days=random.randint(0,36500))).strftime("%Y-%m-%d"),
        style="EU"
    )
    return put

@pytest.fixture
def spot(option):
    spot = option.strike + random.random() * random.choice((-1, 1))
    return spot

@pytest.fixture
def riskfree():
    riskfree = random.random()
    return riskfree

@pytest.fixture
def dividend():
    dividend = random.random()
    return dividend

@pytest.fixture
def volatility():
    volatility = random.random()
    return volatility
