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
