from source_py.simulation.lattice import Lattice
import pytest
import os
import glob
import json

from source_py.simulation.percolation_sq_lattice_L0 import SitePercolationL0


def get_file_list():
    data_dir = "../data_pytest/"
    print(os.listdir(data_dir))
    signature = "SitePercolationL0__percolation_cross_check_data_L*"
    files = glob.glob(data_dir + signature)
    return files


def test_L0_for_all_files():
    files = get_file_list()
    print(files)
    for file in files:
        with open(file) as f:
            line = f.readline()
            header = json.loads(line)
            pass
        print(header)
        LL = header["length"]
        site_id_sequence = header["site_id_sequence"]
        site_index_sequence = header["site_index_sequence"]
        pc = header["pc"]
        site_count_wrapping_cluster_pc = header["site_count_wrapping_cluster_pc"]
        bond_count_wrapping_cluster_pc = header['bond_count_wrapping_cluster_pc']
        entropy_list = header['entropy_list']
        order_largest_list = header['order_largest_list']
        order_wrapping_list = header['order_wrapping_list']

        percolation = SitePercolationL0(length=LL)

        # percolation.set_custome_site_id_list(site_id_sequence)
        percolation.set_custome_site_index_list(site_index_sequence)
        # percolation.viewCluster()
        # percolation.viewLattice()
        percolation.run_once()


        pc_tmp = percolation.get_pc()
        assert abs(pc - pc_tmp) < 1e-6
        tmp_site_count = percolation.get_site_count_wrapping_cluster_pc()
        assert tmp_site_count == site_count_wrapping_cluster_pc
        tmp_bond_count = percolation.get_bond_count_wrapping_cluster_pc()
        assert tmp_bond_count == bond_count_wrapping_cluster_pc

        H_temp = percolation.get_entropy_array()
        P1_temp = percolation.get_order_param_largest_array()
        P2_temp_list = percolation.get_order_param_wrapping_array()
        for i in range(len(entropy_list)):
            assert entropy_list[i] == H_temp[i]
            assert order_largest_list[i] == P1_temp[i]
            assert order_wrapping_list[i] == P2_temp_list[i]
            pass
        print("file ", file, " passed the test")






    pass
