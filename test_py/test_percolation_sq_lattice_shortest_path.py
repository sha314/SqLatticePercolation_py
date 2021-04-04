from source_py.simulation.percolation_sq_lattice_shortest_path import ShortestPathAfter_pc
import pytest

def test_custome_lattice():
    length = 6
    first_col = [0, 5, 10, 15, 20]
    first_row = [0, 1, 2, 3, 4]

    third_col = [i+3 for i in first_col]
    third_row = [i+3*5 for i in first_row]

    ids = third_row + [2, 6, 9]

    # ids = [0, 6, 12, 18, 24, 30, 1, 13, 2, 8, 14, 20, 26, 3, 9, 15, 27, 5, 11, 34, 28, 16]



    ids = list(set(ids))  # to remove repetition
    print("ids ", ids)
    ids.remove(15)
    seed = 72
    percolation = ShortestPathAfter_pc(length=length, seed=seed)
    percolation.set_custome_site_id_list(ids)
    percolation.run_once()
    percolation.viewLattice(2)
    percolation.viewLattice(3)

    print(percolation.get_shortest_path_p())
    flag1 = percolation.scan_all_rows()
    flag2 = percolation.scan_all_cols()
    if percolation.get_shortest_path_p() == 0:

        assert not flag1 and not flag2
    else:
        assert not flag1 or not flag2

    pass

def test_single():
    # test_large_lattice(100, 240)
    test_large_lattice(6, 72)

    pass
def test_multiple_seeds():
    import random
    length = 6
    seedlist = [random.randint(0, 1000) for _ in range(100)]
    print(seedlist)
    for seed in seedlist:
        print("current seed ", seed)
        test_large_lattice(length, seed)

@pytest.mark.parametrize(
    'length, seed',
    ([(20, 363), (25, 0), (50, 200)])
)
def test_large_lattice(length, seed):

    percolation = ShortestPathAfter_pc(length=length, seed=seed)
    percolation.run_once()
    # percolation.viewLattice(2)
    # percolation.viewLattice(3)

    print(percolation.get_shortest_path_p())
    flag1 = percolation.scan_all_rows()
    print("row scan ", flag1)
    flag2 = percolation.scan_all_cols()
    print("col scan ", flag2)
    if percolation.get_shortest_path_p() == 0:
        assert not flag1 and not flag2
    else:
        assert flag1 or flag2
        pass
    pass
