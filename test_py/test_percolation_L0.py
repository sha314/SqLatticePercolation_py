from source_py.percolation_sq_lattice_L0 import SitePercolationL0


def test_simulation_L0_seed(length=6, seed=310):
    percolation = SitePercolationL0(length=length, seed=seed)


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

def test_simulation_L0_reset():
    seed = 310
    length = 6
    percolation = SitePercolationL0(length=length, seed=seed)

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
def test_simulation_L0_different_seeds():
    """
        run simulation for site percolation on square lattice.
        """


    seeded = 310
    length = 6
    for seeded in range(1000):
        test_simulation_L0_seed(length, seeded)
        pass

# pytest fails for L=6, seed=310 for L0
def test_simulation_L0_different_lengths():
    """
        run simulation for site percolation on square lattice.
        """

    length = 10
    seeded = 310
    for length in range(5, 50):
        print("seed ={:4}".format(seeded))
        percolation = SitePercolationL0(length=length, seed=seeded)
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