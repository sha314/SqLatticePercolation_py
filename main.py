import time
from datetime import datetime
import multiprocessing

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


def print_hi():
    from main_py import lattice
    lattice.test(5)
    # lattice.test_neighbors(6)

    from main_py import percolation_sq_lattice
    # percolation_sq_lattice.test_site_percolation()
    # percolation_sq_lattice.test_relative_index()
    percolation_sq_lattice.test_detect_wrapping()

    # import time
    # start_t = time.time()
    # percolation_sq_lattice.test_large(100)
    # end_t = time.time()
    # print("time required ", (end_t - start_t), " sec")

def run_simulation_threads():
    from main_py import ensemble
    lengths = [200, 300, 400]
    En = 500

    from threading import Thread
    from time import sleep

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
    from main_py import ensemble
    length = 10
    thread_counts = 2
    En = 1000
    En_per_thread = En // thread_counts

    from threading import Thread
    from time import sleep

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

def run_simulation_threads_v3():
    from main_py import ensemble
    length = 10
    thread_counts = 2
    En = 1000
    En_per_thread = En // thread_counts

    from threading import Thread
    from time import sleep

    all_processes = []

    for i in range(thread_counts):
        # inargs = {'length':LL, "ensembleSize":En, "thread_count":i}
        process = multiprocessing.Process(target=ensemble.run_ensemble_entropy_order_threads,args=(length, En_per_thread, i))
        all_processes.append(process)
        process.start()

        pass
    for process in all_processes:
        process.join()
        pass


def run_simulations():
    from main_py import ensemble
    LL = 100
    En = 10
    ensemble.run_ensemble_entropy_order(LL, En)

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    time_a = time.time()

    # print_hi()
    # run_simulations()
    # run_simulation_threads()
    # run_simulation_threads_v2()
    run_simulation_threads_v3()

    print("No errors")
    total_time_spent = time.time() - time_a
    if total_time_spent < 10:
        print("Total time elapsed {:2.6f} sec".format(total_time_spent))
        pass
    else:
        hhh = int(total_time_spent)//3600
        total_time_spent = total_time_spent - hhh*3600
        mmm = int(total_time_spent) // 60
        sss = total_time_spent - mmm * 60
        print("Total time elapsed {}h {}m {:.4f}s".format(hhh, mmm, sss))
    now = datetime.now()
    current_time = now.strftime("%Y.%m.%d %H:%M:%S")
    print("Current Time ", current_time)

