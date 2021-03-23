from source_py.percolation_sq_lattice_shortest_path import ShortestPathAfter_pc


def run_shortest_path():
    seed = 310
    length = 6
    percolation = ShortestPathAfter_pc(length=length, seed=seed)
    percolation.run_once()
    pass