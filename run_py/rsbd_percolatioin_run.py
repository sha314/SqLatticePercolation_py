import multiprocessing
import logging
from datetime import datetime
import numpy as np
import json


from source_py.simulation import percolation_sq_lattice_L1L2

def single_realization(percolationClass, length):
    """
    single realization for storing data for future.
    pytest will test using it as reference.
    """
    # print("length ", ensembleSize)
    # print("ensembleSize ", ensembleSize)
    # print("thread_count ", thread_count)


    percolation = percolationClass(length=length)

    percolation.reset()
    # percolation.viewCluster()
    # percolation.viewLattice()
    percolation.run_once()

    # print(data)
    signature = percolation.get_signature()
    now = datetime.now()
    current_time = now.strftime("%Y%m%d_%H%M%S")
    print("current_time ", current_time)

    signature += "_percolation_cross_check_data_L{}_".format(length)
    filename = signature + current_time

    filename += ".txt"
    head = dict()
    head['length'] = length
    head['L'] = length
    head['site_id_sequence'] = percolation.get_site_id_sequence()
    head['site_index_sequence'] = percolation.get_index_sequence()
    head['pc'] = percolation.get_pc()
    head['site_count_wrapping_cluster_pc'] = percolation.get_site_count_wrapping_cluster_pc()
    head['bond_count_wrapping_cluster_pc'] = percolation.get_bond_count_wrapping_cluster_pc()
    head['entropy_list'] = percolation.get_entropy_array()
    head['order_largest_list'] = percolation.get_order_param_largest_array()
    head['order_wrapping_list'] = percolation.get_order_param_wrapping_array()
    head['date'] = now.strftime("%Y.%m.%d")
    head['time'] = now.strftime("%H:%M:%S")
    head['columns'] = ["p", "H", "P1", "P2"]
    head['desc'] = ["p=occupation probability", "H=entropy",
                    "P1=order parameter by wrapping cluster", "P2=order parameter by largest cluster"]
    header_str = json.dumps(head)
    filename = "./data/" + filename
    with open(filename, 'w') as f:
        f.write(header_str)
        pass



    pass

def run_simulation_threads():
    from run_py import ensemble
    lengths = [200, 300, 400]
    En = 500

    from threading import Thread

    i = 0
    all_threads = []
    for LL in lengths:
        # inargs = {'length':LL, "ensembleSize":En, "thread_count":i}
        thread = Thread(target=ensemble.run_ensemble_entropy_order_threads, args=(LL, En, i))
        i += 1
        all_threads.append(thread)
        thread.start()
        pass
    for thread in all_threads:
        thread.join()
        pass

def run_simulation_threads_v2():
    from run_py import ensemble
    length = 10
    thread_counts = 2
    En = 1000
    En_per_thread = En // thread_counts

    from threading import Thread

    all_threads = []
    for i in range(thread_counts):
        # inargs = {'length':LL, "ensembleSize":En, "thread_count":i}
        thread = Thread(target=ensemble.run_ensemble_entropy_order_threads, args=(length, En_per_thread, i))
        all_threads.append(thread)
        thread.start()
        pass
    for thread in all_threads:
        thread.join()
        pass

def run_simulation_threads_v3(length, ensemble_count, thread):
    from run_py import ensemble
    from source_py.simulation import percolation_sq_lattice_L0
    percolationClass = percolation_sq_lattice_L0.SitePercolationL0
    #percolationClass = percolation_sq_lattice_L1L2.SitePercolationL1
    #percolationClass = percolation_sq_lattice_L1L2.SitePercolationL2
    # length = 500
    thread_counts = thread
    En = ensemble_count
    En_per_thread = En // thread_counts

    all_processes = []

    for i in range(thread_counts):
        # inargs = {'length':LL, "ensembleSize":En, "thread_count":i}
        process = multiprocessing.Process(target=ensemble.run_ensemble_entropy_order_threads_v2,
                                          args=(percolationClass, length, En_per_thread, i))
        all_processes.append(process)
        process.start()

        pass
    for process in all_processes:
        process.join()
        pass

def run_simulation_threads_v4(length, ensemble_count, thread, interaction=0):
    from run_py import ensemble
    from source_py.simulation import percolation_sq_lattice_L0
    if interaction == 1:
        percolationClass = percolation_sq_lattice_L1L2.SitePercolationL1
    elif interaction == 2:
        percolationClass = percolation_sq_lattice_L1L2.SitePercolationL2
    else:
        percolationClass = percolation_sq_lattice_L0.SitePercolationL0
    pass

    # length = 500
    thread_counts = thread
    En = ensemble_count
    En_per_thread = En // thread_counts

    all_processes = []

    for i in range(thread_counts):
        # inargs = {'length':LL, "ensembleSize":En, "thread_count":i}
        process = multiprocessing.Process(target=ensemble.run_ensemble_entropy_order_threads_v2,
                                          args=(percolationClass, length, En_per_thread, i))
        all_processes.append(process)
        process.start()

        pass
    for process in all_processes:
        process.join()
        pass


def run_simulations():
    from run_py import ensemble
    from source_py.simulation import percolation_sq_lattice_L0
    LL = 5
    En = 100
    # ensemble.run_ensemble_entorpy_order(percolation_sq_lattice_L0.SitePercolationL0, LL, En)
    # ensemble.run_ensemble_entropy_order(percolation_sq_lattice_L1L2.SitePercolationL1, LL, En)
    # ensemble.run_ensemble_entropy_order(percolation_sq_lattice_L1L2.SitePercolationL2, LL, En)
    ensemble.run_ensemble_entropy_order_threads_v2(percolation_sq_lattice_L0.SitePercolationL0, LL, En, seed=0)