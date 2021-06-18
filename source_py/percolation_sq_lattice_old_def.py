from source_py import lattice
from source_py import cluster
import random
import math
import numpy as np
from source_py.index import *
import gc
# import unittest
import pytest

from source_py.percolation_sq_lattice import SitePercolation
from source_py.simulation.states import SelectionState
import logging
import tensorflow as tf
import time

Lattice = lattice.Lattice
ClusterPool = cluster.ClusterPool

class SitePercolation_old_def(SitePercolation):
    def __init__(self, **kwargs):
        super(SitePercolation_old_def, self).__init__(**kwargs)
        self.signature = "SitePercolationOldDef"
        self.max_entropy = math.log(self.lattice_ref.site_count)
        self.entropy_value = 0
        self.tv1 = 0
        self.tv3 = 0

        gpus = tf.config.list_physical_devices('GPU')
        if gpus:
            try:
                # Currently, memory growth needs to be the same across GPUs
                for gpu in gpus:
                    tf.config.experimental.set_memory_growth(gpu, True)
                # logical_gpus = tf.config.experimental.list_logical_devices('GPU')
                # print(len(gpus), "Physical GPUs,", len(logical_gpus), "Logical GPUs")
            except RuntimeError as e:
                # Memory growth must be set before GPUs have been initialized
                print(e)
        pass

    def reset(self):
        """
        reset for next
        """
        super(SitePercolation_old_def, self).reset()
        self.entropy_value = 0

    def get_cluster_size(self, cluster_id):
        """
        In new definition of site percolation, cluter size id defined by the number of bonds in the cluster.
        Initially all cluster contains exactly 1 bonds.

        Just changing this definition will change the definition of cluster and hence the definition of site percolation itself

        return : number of site in the cluster, max cluster size
        """
        s_count = self.cluster_pool_ref.get_cluster_site_count(cluster_id)
        # normalizer = self.lattice_ref.site_count
        normalizer = self.occupied_site_count
        # print("normalizer ", normalizer)
        return s_count, normalizer

    def entropy(self):
        """
        fast entropy method will not work in old definition
        """
        with tf.device('/GPU:0'):
            H = self.entropy_v3()
        return H.numpy()

    def entropy_time(self):
        t = time.time()
        a = self.entropy_v1()
        self.tv1 += time.time() - t

        t = time.time()
        with tf.device('/GPU:0'):
            b = self.entropy_v3()
        self.tv3 += time.time() - t

        # print("v1a ", a, " time ", self.tv1)
        # print("v3b ", b, " time ", self.tv3)

        pass

    # @tf.function
    def entropy_v3(self):
        """
        tensorflow version. runs on the gpu.

        For L=100 and one realization it tool ~10 sec for V3 but ~100 sec for V1.
        TF made it 10X faster.
        """
        # print("Entry : entropy_v1 <<< ")
        H = 0
        mu_sum = 0
        for i in range(self.cluster_count):
            # b_count = self.cluster_pool_ref.get_cluster_bond_count(i)
            b_count, normalizer = self.get_cluster_size(i)
            mu = b_count / normalizer
            mu_sum += mu
            if mu == 0:
                # print("empty cluster")
                continue
            # print("v1mu = ", mu)
            # self.cluster_pool_ref.get_cluster(i).view()
            log_mu = tf.math.log(mu)
            H += mu * log_mu
            pass
        # self.entropy_value = -H
        # return self.entropy_value
        # assert abs(mu_sum - 1) < 1e-6
        # print("Exit : entropy_v1 >>>")
        return -H

    def order_param_largest_clstr(self):
        _, normalizer = self.get_cluster_size(0)
        return self.largest_cluster_sz / normalizer

    # def order_param_wrapping(self):
    #     if self.after_wrapping:
    #         # print("wrapping cluster id ", self.wrapping_cluster_id)
    #         # count = self.cluster_pool_ref.get_cluster_bond_count(self.wrapping_cluster_id)
    #         count = self.get_cluster_size(self.wrapping_cluster_id)
    #         ret_val = count / self.lattice_ref.site_count
    #         # print("wrapping cluster size ", count, " P = ", ret_val)
    #         return ret_val
    #     return 0.
    #     pass

    def place_one_site(self):
        # print("************************ place_one_site. count ", self.current_idx + 1)
        self.selection_flag = self.select_site()
        if self.selection_flag == SelectionState.SUCESS:

            # print("selected site ", self.current_site.get_index(), " id ", self.current_site.get_id())
            self.lattice_ref.init_relative_index(self.selected_id)  # initialize relative index
            bond_neighbors = self.current_site.connecting_bonds()
            # site_neighbors = self.get_connected_sites(self.current_site, bond_neighbors)

            merged_cluster_index = self.merge_clusters_v2(bond_neighbors)

            self.track_largest_cluster(merged_cluster_index)

            # self.lattice_ref.set_site_gid_by_id(selected_id, merged_cluster_index)
            # self.cluster_pool_ref.add_sites(merged_cluster_index, selected_id)

            pass
        elif self.selection_flag == SelectionState.CURRENT_SITE_NOT_EMPTY:
            # print("current site is not empty but there are empty sites in the lattice")
            pass
        elif self.selection_flag == SelectionState.EMPTY_SITE_LIST:
            # print("No remaining empty sites")
            return False
        return True

    def test_clusters(self):
        # for unit test. At the end of a simulation
        if self.occupied_site_count < self.lattice_ref.site_count:
            return


        bond_ids_indices = list(range(0, 2*self.lattice_ref.length ** 2))
        bsum = ssum = 0
        for gid in bond_ids_indices:
            b1 = self.cluster_pool_ref.get_cluster_bond_count(gid)
            s1 = self.cluster_pool_ref.get_cluster_site_count(gid)
            if gid == self.wrapping_cluster_id:
                assert b1 == self.lattice_ref.bond_count
                assert s1 == self.lattice_ref.site_count
                pass
            else:
                bsum += b1
                ssum += s1
                pass
            pass
        # no sites or bonds in other clusters
        assert bsum == 0
        assert ssum == 0
        assert self.largest_cluster_sz == self.lattice_ref.length ** 2

        self.cluster_pool_ref.test_cluster()


if __name__ == '__main__':
    print("Speed test of tensorflow")
    tf.debugging.set_log_device_placement(True)
    percolation = SitePercolation_old_def(length=100)

    percolation.reset()
    while percolation.place_one_site():
        # print("self.selection_flag ", self.selection_flag)
        if percolation.selection_flag == SelectionState.SUCESS:
            # percolation.detect_wrapping()
            # p = percolation.occupation_prob()
            # print("p = ", p)
            H = percolation.entropy_time()
            pass
        pass
    print("v1 ", percolation.tv1)
    print("v3 ", percolation.tv3)
