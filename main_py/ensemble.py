from main_py.percolation_sq_lattice import SitePercolation_L1
from datetime import datetime
import json
import numpy as np
import time

def run_ensemble_entropy_order(length, ensembleSize, interaction=0):
    """
    run simulation for site percolation on square lattice.
    """

    percolation = SitePercolation_L1(length=length)
    data = None
    for en in range(ensembleSize):
        start_t = time.time()

        percolation.reset()

        percolation.run_once()
        aaa = percolation.get_data_array()
        if data is None:
            data = aaa
        else:
            data += aaa
            pass
        pass
        print("temp ")
        print(aaa)
        end_t = time.time() - start_t
        print("Iteration {:4f} | Time elapsed {:.5f} sec".format(en, end_t))
        pass

    data /= ensembleSize  # taking average
    # print(data)
    signature = percolation.get_signature()
    signature += "_entropy_order_"
    now = datetime.now()
    current_time = now.strftime("%Y%m%d_%H%M%S")
    print("current_time ", current_time)
    filename = signature + current_time + ".txt"

    head = dict()
    head['length'] = length
    head['L'] = length
    head['ensemble_size'] = ensembleSize
    head['En'] = ensembleSize
    head['date'] = now.strftime("%Y.%m.%d")
    head['time'] = now.strftime("%H:%M:%S")
    head['columns'] = ["p", "H", "P1", "P2"]
    head['desc'] = ["p=occupation probability", "H=entropy",
                    "P1=order parameter by wrapping cluster", "P2=order parameter by largest cluster"]
    header_str = json.dumps(head)

    filename = "./data/" + filename
    np.savetxt(filename, data, fmt="%.10e", header=header_str)


    pass
