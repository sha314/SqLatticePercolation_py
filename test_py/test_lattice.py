from source_py.lattice import Lattice
import pytest

# def test(length):
#     lattice = Lattice(length)
#     lattice.view(0)
#     lattice.view(1)
#     lattice.view(2)
#     # print(lattice.get_row_str(0))



@pytest.mark.parametrize(
    'length',
    ([4, 6, 7, 8, 9, 10])
)
def test_neighbors(length):
    lattice = Lattice(length)
    # lattice.view(0)
    # lattice.view(1)
    # lattice.view(2)
    #
    # lattice.list_all_sites()
    # lattice.list_all_bonds()

    lattice.scan_sites()
    lattice.scan_bonds()
    # print(lattice.get_neighbor_bonds(0))
    # print(lattice.get_neighbor_bonds(2))
    # print(lattice.get_neighbor_bonds(5))
    # print(lattice.get_neighbor_bonds(13))
    # print(lattice.get_neighbor_bonds(19))
    # print(lattice.get_neighbor_sites(5))
    # print(lattice.get_neighbor_sites(8))
    # print(lattice.get_neighbor_sites(50))
    pass
