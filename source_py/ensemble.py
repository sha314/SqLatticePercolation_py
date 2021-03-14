# from source_py.percolation_sq_lattice import SitePercolationL0
from source_py.percolation_sq_lattice_L0 import SitePercolationL0
from datetime import datetime
import json
import numpy as np
import time

def run_ensemble_entropy_order(percolationClass, length, ensembleSize, interaction=0):
    """
    run simulation for site percolation on square lattice.
    """

    percolation = percolationClass(length=length)
    data = None
    pcs = []
    for en in range(ensembleSize):
        start_t = time.time()

        percolation.reset()
        # percolation.viewCluster()
        # percolation.viewLattice()
        percolation.run_once()
        pcs.append(percolation.get_tc())
        aaa = percolation.get_data_array()
        print(aaa[-1,:])
        if data is None:
            data = aaa
        else:
            data += aaa
            pass
        pass
        # print("temp ")
        # print(aaa)
        end_t = time.time() - start_t
        print("Iteration {:4} | Time elapsed {:.5f} sec".format(en, end_t))
        pass

    data /= ensembleSize  # taking average
    # print(data)
    signature = percolation.get_signature()
    now = datetime.now()
    current_time = now.strftime("%Y%m%d_%H%M%S")
    print("current_time ", current_time)

    write_entropy_order(current_time, data, ensembleSize, length, now, signature)
    write_pc_values(current_time, pcs, ensembleSize, length, now, signature)
    pass


def write_entropy_order(current_time, data, ensembleSize, length, now, signature, thread_count=None):
    signature += "_entropy_order_L{}_".format(length)
    filename = signature + current_time
    if thread_count is not None:
        filename += "_th{}".format(thread_count)
        pass
    filename += ".txt"
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


def write_pc_values(current_time, data, ensembleSize, length, now, signature, thread_count=None):
    signature += "_pc_values_L{}_".format(length)
    filename = signature + current_time
    if thread_count is not None:
        filename += "_th{}".format(thread_count)
        pass
    filename += ".txt"
    head = dict()
    head['length'] = length
    head['L'] = length
    head['ensemble_size'] = ensembleSize
    head['En'] = ensembleSize
    head['date'] = now.strftime("%Y.%m.%d")
    head['time'] = now.strftime("%H:%M:%S")
    head['columns'] = ["pc"]
    head['desc'] = ["pc=critical ocupation probability"]
    header_str = json.dumps(head)
    filename = "./data/" + filename
    np.savetxt(filename, data, fmt="%.10e", header=header_str)


def run_ensemble_entropy_order_threads(percolationClass, length, ensembleSize, thread_count=0):
    """
    run simulation for site percolation on square lattice.
    """
    # print("length ", ensembleSize)
    # print("ensembleSize ", ensembleSize)
    # print("thread_count ", thread_count)

    percolation = percolationClass(length=length)
    data = None
    for en in range(1, ensembleSize+1):
        start_t = time.time()

        percolation.reset()
        # percolation.viewCluster()
        # percolation.viewLattice()
        percolation.run_once()
        aaa = percolation.get_data_array()
        if data is None:
            data = aaa
        else:
            data += aaa
            pass
        pass
        # print("temp ")
        # print(aaa)
        del aaa
        end_t = time.time() - start_t
        print("Iteration {:4} | Time elapsed {:.5f} sec | thread {:2} "
              .format(en*(thread_count+1), end_t, thread_count))
        pass

    data /= ensembleSize  # taking average
    # print(data)
    signature = percolation.get_signature()
    signature += "_entropy_order_L{}_".format(length)
    now = datetime.now()
    current_time = now.strftime("%Y%m%d_%H%M%S")
    print("current_time ", current_time)
    filename = signature + current_time
    if thread_count is not None:
        filename += "_th{}".format(thread_count)
        pass
    filename += ".txt"

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


def run_ensemble_entropy_order_threads_v2(percolationClass, length, ensembleSize, thread_count=0):
    """
    run simulation for site percolation on square lattice.
    """
    # print("length ", ensembleSize)
    # print("ensembleSize ", ensembleSize)
    # print("thread_count ", thread_count)

    percolation = percolationClass(length=length)
    data = None
    pcs = []
    for en in range(1, ensembleSize+1):
        start_t = time.time()

        percolation.reset()
        # percolation.viewCluster()
        # percolation.viewLattice()
        percolation.run_once()
        pcs.append(percolation.get_tc())
        aaa = percolation.get_data_array()
        if data is None:
            data = aaa
        else:
            data += aaa
            pass
        pass
        # print("temp ")
        # print(aaa)
        del aaa
        end_t = time.time() - start_t
        print("Iteration {:4} | Time elapsed {:.5f} sec | thread {:2} "
              .format(en*(thread_count+1), end_t, thread_count))
        pass

    data /= ensembleSize  # taking average
    # print(data)
    signature = percolation.get_signature()
    now = datetime.now()
    current_time = now.strftime("%Y%m%d_%H%M%S")
    print("current_time ", current_time)

    write_entropy_order(current_time, data, ensembleSize, length, now, signature, thread_count=thread_count)
    write_pc_values(current_time, pcs, ensembleSize, length, now, signature, thread_count=thread_count)
    pass


    pass
