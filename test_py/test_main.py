import time
from datetime import datetime
import multiprocessing

def test_L0():
    print("Unit Test using pytest")
    from test_py import test_percolation_L0
    # test_percolation_L0.test_simulation_L0_different_seeds()
    # test_percolation_L0.test_simulation_L0_different_lengths()
    test_percolation_L0.test_simulation_L0_seed(length=6, seed=41)
    # test_percolation_L0.test_simulation_L0_reset()  # TODO
    pass


