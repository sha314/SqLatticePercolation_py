from source_py.simulation.percolation_sq_lattice_L0 import SitePercolationL0
import pytest

from source_py.simulation.percolation_sq_lattice_L1L2 import SitePercolationL1


def test_simulation_L1_seed(length=6, seed=310):
    percolation = SitePercolationL1(length=length, seed=seed)


    # percolation.viewCluster()
    # percolation.viewLattice()
    P1 = -222
    site_count = 1
    percolation.test_lattice()
    while percolation.place_one_site():
        percolation.detect_wrapping()
        print("occupied ", site_count, " sites")
        percolation.viewLattice(3)
        # percolation.viewLattice(1)
        percolation.test_lattice()
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
    percolation.viewLattice(3)
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

def test_simulation_L1_reset():
    seed = 310
    length = 6
    percolation = SitePercolationL1(length=length, seed=seed)

    percolation.reset()  # must be tested  <<<<< TODO
    # percolation.viewCluster()
    # percolation.viewLattice()
    P1 = -222
    while percolation.place_one_site():
        percolation.detect_wrapping()
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
        pass
    if P1 != 1.0:
        print("P1 should be 1.0")
    assert P1 == 1.0
    percolation.viewLattice()
    percolation.viewLattice(3)
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

# pytest fails for L=6, seed=310 for L0
def test_simulation_L1_different_seeds():
    """
        run simulation for site percolation on square lattice.
        """


    seeded = 310
    length = 6
    import random
    seed_list = [random.seed(0, 1000) for _ in range(10)]
    for seeded in seed_list:
        test_simulation_L1_seed(length, seeded)
        pass

# pytest fails for L=6, seed=310 for L0
def test_simulation_L1_different_lengths():
    """
        run simulation for site percolation on square lattice.
        """
    seeded = 310
    import random
    length_list = [random.randint(5, 50) for _ in range(10)]
    for length in length_list:
        print("seed ={:4}".format(seeded))
        percolation = SitePercolationL1(length=length, seed=seeded)
        data = None
        pcs = []

        percolation.reset()
        # percolation.viewCluster()
        # percolation.viewLattice()
        percolation.run_once()
        # pcs.append(percolation.get_tc())
        # aaa = percolation.get_data_array()
        # assert aaa[-1, -2] == 1.0
        # if aaa[-1, -2] == 1:
        #     break
        # print(aaa[-1, -2])
        percolation.test_clusters()
        percolation.test_lattice()
        pass
    # print("seed ={:4}".format(seeded))


    pass


@pytest.mark.parametrize(
    "length, seeded",
    ([(6, 310),
      (7, 8),
      (9, 10)])
)
def test_simulation_L1_different_lengths_parametrize(length, seeded):
    """
        run simulation for site percolation on square lattice.
        """

    print("seed ={:4}".format(seeded))
    percolation = SitePercolationL1(length=length, seed=seeded)

    percolation.run_once()
    percolation.test_clusters()
    percolation.test_lattice()

    percolation.reset()

    percolation.run_once()
    percolation.test_clusters()
    percolation.test_lattice()

    pass
    # print("seed ={:4}".format(seeded))

def custome_lattice_config_1():
    """
    A wrapping in the end
    L=6
    full lattice
    0, 1, 2, 3, 4, 5,
    6, 7, 8, 9, 10, 11,
    12, 13, 14, 15, 16, 17,
    18, 19, 20, 21, 22, 23,
    24, 25, 26, 27, 28, 29,
    30, 31, 32, 33, 34, 35

    selected ids
    -, -, *, -, -, -,
    -, -, *, -, -, -,
    -, -, *, -, -, -,
    -, *, *, -, -, -,
    #, *, #, *, *, *,
    -, -, -, -, *, *,

    occupy the # site at last
    """
    length = 6
    ids = [2, 8, 14, 19, 20, 25, 27, 28, 29, 34, 35]
    special_ids = [26, 24]

    import random
    seed = random.randint(0, 10000)
    percolation = SitePercolationL0(length=length, seed=seed)
    percolation.set_custome_site_id_list(ids, True)
    while percolation.place_one_site():
        pass
    # percolation.viewLattice(2)
    percolation.viewLattice(3)

    ## enter the special site
    percolation.set_custome_site_id_list(ids + special_ids, False)  # since only the new ids will be placed
    while percolation.place_one_site():
        pass
    # percolation.viewLattice(2)
    percolation.viewLattice(3)
    assert percolation.detect_wrapping()


    pass

def custome_lattice_config_2():
    """
    cluster labeling
    L=6
    full lattice
    0, 1, 2, 3, 4, 5,
    6, 7, 8, 9, 10, 11,
    12, 13, 14, 15, 16, 17,
    18, 19, 20, 21, 22, 23,
    24, 25, 26, 27, 28, 29,
    30, 31, 32, 33, 34, 35

    selected ids
    -, -, *, -, -, -,
    -, -, *, -, -, -,
    -, -, *, -, -, -,
    -, *, *, -, -, -,
    -, *, *, *, *, *,
    -, -, -, -, *, *,

    occupy the # site at last
    """
    length = 6
    ids = [2, 8, 14, 19, 20, 25, 27, 28, 29, 34, 35, 26]

    import random
    seed = random.randint(0, 10000)
    percolation = SitePercolationL1(length=length, seed=seed)
    percolation.set_custome_site_id_list(ids, True)
    while percolation.place_one_site():
        pass
    # percolation.viewLattice(2)
    percolation.viewLattice(3)


    pass

def test_custome_lattices():
    for i in range(100):
        custome_lattice_config_1()
    # custome_lattice_config_2()


    pass