# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


def print_hi():
    from main_py import lattice
    # lattice.test(5)
    # lattice.test_neighbors(6)

    from main_py import percolation_sq_lattice
    # percolation_sq_lattice.test_site_percolation()
    # percolation_sq_lattice.test_relative_index()
    # percolation_sq_lattice.test_detect_wrapping()
    import time
    start_t = time.time()
    percolation_sq_lattice.test_large(8)
    end_t = time.time()
    print("time required ", (end_t - start_t), " sec")

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi()
    print("No errors")
