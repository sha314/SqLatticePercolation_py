from source_py.lattice import Lattice
from source_py.percolation_sq_lattice_L0 import SitePercolationL0
import pytest
import random

from source_py.percolation_sq_lattice_old_def import SitePercolation_old_def


def test_simulation_L0OldDef_seed(length=6, seed=310):
    percolation = SitePercolation_old_def(length=length, seed=seed)

    # percolation.viewCluster()
    # percolation.viewLattice()
    P1 = -222
    site_count = 1
    percolation.test_lattice()
    while percolation.place_one_site():
        percolation.detect_wrapping()
        print("occupied ", site_count, " sites")
        # percolation.viewLattice(3)
        # percolation.viewLattice(1)
        percolation.test_lattice()
        percolation.test_clusters()
        percolation.test_entropy()
        P1 = percolation.order_param_wrapping()
        # print("p= ", percolation.occupation_prob(),
        #       " entropy_v1 ", percolation.entropy_v1(),
        #       " entropy_v2 ", percolation.entropy_v2(),
        #       " order wrapping ", percolation.order_param_wrapping(),
        #       " order largest ", percolation.order_param_largest_clstr())
        # percolation.viewLattice(3)
        # percolation.viewCluster()
        # if percolation.detect_wrapping():
        #     print("Wrapping detected")
        #     break
        site_count += 1
        pass
    if P1 != 1.0:
        print("P1 should be 1.0")
    assert P1 == 1.0
    # percolation.viewLattice()
    # percolation.viewLattice(3)
    percolation.test_clusters()
    percolation.test_lattice()
    # percolation.viewCluster()
    # percolation.viewLattice()
    # pcs.append(percolation.get_tc())
    # aaa = percolation.get_data_array()
    # print(aaa)
    # assert aaa[-1, -2] == 1.0
    # if aaa[-1, -2] == 1:
    #     break
    # print(aaa[-1, -2])


def test_simulation_L0OldDef_seed_and_L_sets():
    count = 10
    seed_list = [random.randint(0, 1000) for _ in range(count)]
    length_list = [random.randint(5, 20) for _ in range(count)]

    for seed, length in zip(seed_list, length_list):
        print("============= Testing with L={},s={}===========".format(length, seed))
        test_simulation_L0OldDef_seed(length, seed)

    pass
