import time
from datetime import datetime
import multiprocessing

def test_L0():
    print("Unit Test using pytest")
    from test_py import test_percolation_L0
    test_percolation_L0.test_simulation_L0()
    test_percolation_L0.test_simulation_L0_seed()
    pass


