from source_py.percolation_sq_lattice_shortest_path import ShortestPathAfter_pc


def run_shortest_path():
    seed = 72
    length = 6
    percolation = ShortestPathAfter_pc(length=length, seed=seed)
    percolation.run_once()
    percolation.viewLattice(3)
    print(percolation.get_shortest_path_p())
    pass

def run_shortest_path_ensemble(length, ensemble_size):
    percolation = ShortestPathAfter_pc(length=length)
    for e in range(1, ensemble_size+1):
        percolation.reset()
        percolation.run_once()
        print("iteration ", e, " p*= ", percolation.get_shortest_path_p())