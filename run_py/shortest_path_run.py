from source_py.simulation.percolation_sq_lattice_shortest_path import ShortestPathAfter_pc
import time
from datetime import datetime
import json
import numpy as np
import multiprocessing


def run_shortest_path():
    seed = 72
    length = 6
    percolation = ShortestPathAfter_pc(length=length, seed=seed)
    percolation.run_once()
    percolation.viewLattice(3)
    print(percolation.get_shortest_path_p())
    pass


def ensemble_shortest_path_v1(length, ensemble_size):
    percolation = ShortestPathAfter_pc(length=length)
    for e in range(1, ensemble_size+1):
        percolation.reset()
        percolation.run_once()
        print("iteration ", e, " p*= ", percolation.get_shortest_path_p())

def write_p_p_star(current_time, data, ensembleSize, length, now, signature, thread_count=2):
    signature += "_shortest_path_p_L{}_".format(length)
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
    head['columns'] = ["pc", "p*"]
    head['desc'] = ["pc=critical ocupation probability",
                    "p*=occupation probability for which the wrapping cluster creates a shortest path for the first "
                    "time"]
    header_str = json.dumps(head)
    filename = "./data/" + filename
    np.savetxt(filename, data, fmt="%.10e", header=header_str)


    pass

def ensemble_shortest_path_v2_thread(percolationClass, length, ensembleSize, thread_count=0, seed=None):
    """
    run simulation for site percolation on square lattice.
    """
    # print("length ", ensembleSize)
    # print("ensembleSize ", ensembleSize)
    # print("thread_count ", thread_count)

    percolation = percolationClass(length=length)
    if seed is not None:
        percolation = percolationClass(length=length, seed=seed)
        pass

    critical_data = []
    for en in range(1, ensembleSize+1):
        start_t = time.time()

        percolation.reset()
        percolation.run_once()
        print("iteration ", en, " p*= ", percolation.get_shortest_path_p())

        critical_data.append([percolation.get_pc(),
                              percolation.get_shortest_path_p(),
                              ])

        end_t = time.time() - start_t
        print("Iteration {:4} | Time elapsed {:.5f} sec | thread {:2} "
              .format(en*(thread_count+1), end_t, thread_count))
        pass


    # print(data)
    signature = percolation.get_signature()
    now = datetime.now()
    current_time = now.strftime("%Y%m%d_%H%M%S")
    print("current_time ", current_time)

    write_p_p_star(current_time, critical_data, ensembleSize, length, now, signature, thread_count=thread_count)
    pass

def run_simulation_shortest_path_threads(length, ensemble_count, thread=2):
    from source_py.simulation import percolation_sq_lattice_shortest_path
    percolationClass = percolation_sq_lattice_shortest_path.ShortestPathAfter_pc
    # length = 500
    thread_counts = thread
    En = ensemble_count
    En_per_thread = En // thread_counts

    all_processes = []

    for i in range(thread_counts):
        # inargs = {'length':LL, "ensembleSize":En, "thread_count":i}
        process = multiprocessing.Process(target=ensemble_shortest_path_v2_thread,
                                          args=(percolationClass, length, En_per_thread, i))
        all_processes.append(process)
        process.start()

        pass
    for process in all_processes:
        process.join()
        pass