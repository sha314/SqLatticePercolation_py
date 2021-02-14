import time
from datetime import datetime


# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


def print_hi():
    from main_py import lattice
    # lattice.test(5)
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


def run_simulations():
    from main_py import ensemble
    LL = 100
    En = 10
    ensemble.run_ensemble_entropy_order(LL, En)

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    time_a = time.time()

    # print_hi()
    run_simulations()

    print("No errors")
    total_time_spent = time.time() - time_a
    print("Total time elapsed {:2.6f} sec".format(total_time_spent))
    now = datetime.now()
    current_time = now.strftime("%Y.%m.%d %H:%M:%S")
    print("Current Time ", current_time)

