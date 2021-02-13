from main_py.percolation_sq_lattice import SitePercolation_L1

def run_ensemble_entropy_order(length, ensembleSize, interaction=0):
    import time

    percolation = SitePercolation_L1(length=length)
    data = None
    for en in range(ensembleSize):
        start_t = time.time()

        percolation.reset()

        percolation.run_once()

        if data is None:
            data = percolation.get_data_array()
        else:
            data += percolation.get_data_array()
            pass
        pass
        end_t = time.time() - start_t
        print("Iteration {:4f} | Time elapsed {:.5f} sec".format(en, end_t))
        pass

    data /= ensembleSize  # taking average
    print(data)

    pass
