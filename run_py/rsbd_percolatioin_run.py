import multiprocessing

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
    from source_py import percolation_sq_lattice_L0
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


def run_simulations():
    from run_py import ensemble
    from source_py import percolation_sq_lattice_L0
    LL = 5
    En = 100
    # ensemble.run_ensemble_entorpy_order(percolation_sq_lattice_L0.SitePercolationL0, LL, En)
    # ensemble.run_ensemble_entropy_order(percolation_sq_lattice_L1L2.SitePercolationL1, LL, En)
    # ensemble.run_ensemble_entropy_order(percolation_sq_lattice_L1L2.SitePercolationL2, LL, En)
    ensemble.run_ensemble_entropy_order_threads_v2(percolation_sq_lattice_L0.SitePercolationL0, LL, En, seed=0)