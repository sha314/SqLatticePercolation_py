# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from run_py.rsbd_percolatioin_run import run_simulation_threads_v3, run_simulation_threads_v4, run_simulations, \
    single_realization
from run_py.shortest_path_run import *
from source_py.simulation import percolation_sq_lattice_L0
import logging


def print_hi():
    from source_py.simulation import lattice
    lattice.test(5)
    lattice.test_neighbors(6)

    # from source_py import percolation_sq_lattice
    # percolation_sq_lattice.test_site_percolation()
    # percolation_sq_lattice.test_relative_index()
    # percolation_sq_lattice.test_detect_wrapping()

    # import time
    # start_t = time.time()
    # percolation_sq_lattice.test_large(100)
    # end_t = time.time()
    # print("time required ", (end_t - start_t), " sec")

    from source_py.simulation import percolation_sq_lattice_L0
    # percolation_sq_lattice_L0.test_detect_wrapping()
    # percolation_sq_lattice_L0.test_relative_index()
    percolation_sq_lattice_L0.test_reset_relative_index()
    # percolation_sq_lattice.test_detect_wrapping()
    # percolation_sq_lattice_L0.test_simulation_L0()


    # from source_py import percolation_sq_lattice_L1L2
    # percolation_sq_lattice.test_site_percolation()
    # percolation_sq_lattice_L1L2.test_L1()
    # percolation_sq_lattice_L1L2.test_L2()
    # percolation_sq_lattice_L1L2.test_detect_wrapping_L1L2()
    # print(2**7)
    # print(2 ** 8)
    # print(2 ** 9)
    # print(2 ** 10)
    pass

def mTests():
    # from source_py.simulation import lattice
    # lattice.mTest_hilight()
    from source_py.simulation import percolation_sq_lattice_L1L2
    percolation_sq_lattice_L1L2.mTest_L1()
    pass

def print_duration(total_time_spent):
    hhh = int(total_time_spent) // 3600
    total_time_spent = total_time_spent - hhh * 3600
    mmm = int(total_time_spent) // 60
    sss = total_time_spent - mmm * 60
    print("Total time elapsed {}h {}m {:.4f}s".format(hhh, mmm, sss))

def init_directories():
    import os
    log_dir = "./logs/"
    if not os.path.isdir(log_dir):
        # print("log directory created")
        os.mkdir(log_dir)
        pass

    data_dir = "./data/"
    if not os.path.isdir(data_dir):
        # print("data directory created")
        os.mkdir(data_dir)
        pass

def init_logging():
    # logging to a file
    now = datetime.now()
    current_time = now.strftime("%Y%m%d_%H%M%S")
    log_dir = "./logs/"

    filename = log_dir + "run_simulation_threads_v4-log-" + current_time + ".txt"

    FORMAT = '[%(asctime)s] %(message)s'
    logging.basicConfig(filename=filename, format=FORMAT, level=logging.DEBUG)

    # logging.info("Testing")
    pass


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    time_a = time.time()

    init_directories()
    init_logging()

    # print_hi()
    # run_simulations()
    # run_simulation_threads()
    # run_simulation_threads_v2()
    # run_simulation_threads_v4(10, 100, 2, interaction=1)

    run_simulation_threads_v4(200, 5000, 20, interaction=1)
    run_simulation_threads_v4(300, 5000, 20, interaction=1)
    run_simulation_threads_v4(400, 5000, 20, interaction=1)
    run_simulation_threads_v4(500, 5000, 20, interaction=1)

    run_simulation_threads_v4(200, 5000, 20, interaction=1)
    run_simulation_threads_v4(300, 5000, 20, interaction=1)
    run_simulation_threads_v4(400, 5000, 20, interaction=1)
    run_simulation_threads_v4(500, 5000, 20, interaction=1)

    # run_simulation_threads_v4(200, 5000, 20, interaction=2)
    # run_simulation_threads_v4(300, 5000, 20, interaction=2)
    # run_simulation_threads_v4(400, 5000, 20, interaction=2)
    # run_simulation_threads_v4(500, 5000, 20, interaction=2)
    #
    # run_simulation_threads_v4(200, 5000, 20, interaction=2)
    # run_simulation_threads_v4(300, 5000, 20, interaction=2)
    # run_simulation_threads_v4(400, 5000, 20, interaction=2)
    # run_simulation_threads_v4(500, 5000, 20, interaction=2)

    # run_simulation_threads_v3(2 ** 7, 5000, 20)  # 128
    # run_simulation_threads_v3(2 ** 8, 5000, 20)  # 256
    # run_simulation_threads_v3(2 ** 9, 5000, 20)  # 512
    # run_simulation_threads_v3(2 ** 10, 6000, 12)  # 1024

    # run_shortest_path()
    # run_shortest_path_ensemble(200, 10)
    # run_simulation_shortest_path_threads(50, 100, thread=2)

    # single_realization(percolation_sq_lattice_L0.SitePercolationL0, 5)

    # from test_py import test_percolation_L1
    # test_percolation_L1.test_simulation_L1_seed()

    # mTests()

    # print("No errors")
    logging.info("No errors")
    total_time_spent = time.time() - time_a
    if total_time_spent < 10:
        log_str = "Total time elapsed {:2.6f} sec".format(total_time_spent)
        # print(log_str)
        logging.info(log_str)
        pass
    else:
        print_duration(total_time_spent)
    now = datetime.now()
    current_time = now.strftime("%Y.%m.%d %H:%M:%S")
    log_str = "Current Time " + current_time
    # print(log_str)
    logging.info(log_str)

