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
        # self.A_site_id_to_cluster_gid = [i for i in range(self.lattice_ref.site_count)]
        # self.B_active_cluster_gid_to_cluster_sizes = [0]*self.lattice_ref.bond_count
        self.cluster_sizes = [0]*self.lattice_ref.bond_count

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
        self.cluster_sizes = [0]*self.lattice_ref.bond_count

    # tf.function
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
            # H = self.entropy_v3()
        return H.numpy()

        # return self.entropy_v4_numpy()

    def entropy_time(self):
        t = time.time()
        a = self.entropy_v1()
        self.tv1 += time.time() - t

        t = time.time()
        with tf.device('/GPU:0'):
            b = self.entropy_v3(self.cluster_sizes)
        self.tv3 += time.time() - t

        # print("v1a ", a, " time ", self.tv1)
        # print("v3b ", b, " time ", self.tv3)

        pass

    @tf.function
    def entropy_v3(self):
        """
        tensorflow version. runs on the gpu.

        For L=100 and one realization it tool ~10 sec for V3 but ~100 sec for V1.
        TF made it 10X faster.
        """
        normalizer = np.sum(self.cluster_sizes)
        clustersizes = np.array(self.cluster_sizes)
        mu_list = clustersizes[clustersizes > 0]/normalizer
        Hlist = np.log(mu_list)*mu_list
        H = -np.sum(Hlist)
        tf.print("entropy ", H)
        return H

    # @tf.function
    # def entropy_v3(self, cluster_sizes):
    #     """
    #     tensorflow version. runs on the gpu.
    #
    #     For L=100 and one realization it tool ~10 sec for V3 but ~100 sec for V1.
    #     TF made it 10X faster.
    #     """
    #     # print("Entry : entropy_v1 <<< ")
    #     H = 0
    #     mu_sum = 0
    #     normalizer = tf.math.reduce_sum(cluster_sizes)
    #     # _, normt = self.get_cluster_size(0)
    #
    #     # tf.print("normalizer = ", normalizer, " normTemp ", normt)
    #     # if normalizer != normt:
    #     #     self.viewCluster()
    #     #     print(cluster_sizes)
    #     #     exit(-1)
    #     #     pass
    #     # cluster_sizes_non_zero = cluster_sizes[cluster_sizes > 0]
    #     for b_count in cluster_sizes:
    #         mu = b_count / normalizer
    #         if mu == 0:
    #             # print("empty cluster")
    #             continue
    #         # print("v1mu = ", mu)
    #         # tf.print("mu = ", mu)
    #         # self.cluster_pool_ref.get_cluster(i).view()
    #         mu_sum += mu
    #         log_mu = tf.math.log(mu)
    #         H += mu * log_mu
    #         pass
    #     # tf.print("mu_sum = ", mu_sum)
    #     # self.entropy_value = -H
    #     # return self.entropy_value
    #     # assert abs(mu_sum - 1) < 1e-6
    #     # print("Exit : entropy_v1 >>>")
    #     return -H

    def entropy_v4_numpy(self):
        """
        tensorflow version. runs on the gpu.

        For L=100 and one realization it tool ~10 sec for V3 but ~100 sec for V1.
        TF made it 10X faster.
        """
        normalizer = np.sum(self.cluster_sizes)
        clustersizes = np.array(self.cluster_sizes)
        mu_list = clustersizes[clustersizes > 0]/normalizer
        Hlist = np.log(mu_list)*mu_list
        H = -np.sum(Hlist)

        return H

    def order_param_largest_clstr(self):
        _, normalizer = self.get_cluster_size(0)
        return self.largest_cluster_sz / normalizer


    def merge_clusters_v3(self, bond_neighbors_unique):
        """
        merging with relabeling relative indices
        """
        bond_gids = self.get_bond_gids(bond_neighbors_unique)
        # site_gids = self.get_site_gids(site_neighbors)
        # print("site_gids ", site_gids)
        # print("bond_gids ", bond_gids)
        # print("set minus ", set(site_gids) - set(bond_gids))
        # print("merging clusters ", bond_gids)
        ref_sz = 0
        root_clstr = bond_gids[0]
        for bbg in bond_gids:
            if self.after_wrapping and (self.wrapping_cluster_id in bond_gids):
                # print("After wrapping, the wrapping cluster is the root cluster even if other involved clusters are larger")
                root_clstr = self.wrapping_cluster_id
                break
            # sz = self.cluster_pool_ref.get_cluster_bond_count(bbg)
            sz = self.get_cluster_size(bbg)[0]
            if sz >= ref_sz:
                root_clstr = bbg
                ref_sz = sz
                pass
            pass
        # print("root cluster is ", root_clstr)
        # print("Assign and relabel currently selected site")
        for bb in bond_neighbors_unique:
            bbg = self.lattice_ref.get_bond_by_id(bb).get_gid()
            if bbg == root_clstr:
                # print("bb ", bbg, " is a root cluster")
                # relabel and assign the current site here
                self.lattice_ref.set_site_gid_by_id(self.selected_id, root_clstr)
                self.cluster_pool_ref.add_sites(root_clstr, self.selected_id)
                # relabeling current site. relative index
                neighbor_site = self.get_neighbor_site(self.current_site.get_id(), bb)
                if self.lattice_ref.get_site_gid_by_id(neighbor_site) >= 0:
                    # relabel selected site with respect to neighbor site. so neighbor_site is the central site
                    rri = self.get_relative_index(neighbor_site, self.selected_id)
                    # rri = self.get_relative_index(self.selected_id, neighbor_site)

                    # sitttte = self.lattice_ref.get_site_by_id(self.selected_id)
                    # print("relative index before ", sitttte.get_relative_index())
                    # print(self.selected_id, " ", sitttte,  " => rri ", rri)

                    self.lattice_ref.set_relative_index(self.selected_id, rri)
                else:
                    # print("does not belong to any cluster yet")
                    pass
                continue
                pass
            pass
        pass
        # print("Relabel all cluster according to root cluster and selected site")
        # print("bond_neighbors size ", len(bond_neighbors))
        for bb in bond_neighbors_unique:
            bbg = self.lattice_ref.get_bond_by_id(bb).get_gid()
            if bbg == root_clstr:

                continue
            # print("relabeling relative index of cluster ", bbg)
            self.relabel_relative_indices(bb)
            # print("merging ", bbg, " to ", root_clstr)
            self.cluster_pool_ref.merge_cluster_with(root_clstr, bbg, self.lattice_ref)
            pass

        # for bbg in bond_gids:
        #     if bbg == root_clstr:
        #         # print("bb ", bbg, " is a root cluster")
        #         continue
        #     self.cluster_pool_ref.clear_cluster(bbg)

        return root_clstr
        pass

    def place_one_site(self):
        # print("************************ place_one_site. count ", self.current_idx + 1)
        self.selection_flag = self.select_site()
        if self.selection_flag == SelectionState.SUCESS:

            # print("selected site ", self.current_site.get_index(), " id ", self.current_site.get_id())
            self.lattice_ref.init_relative_index(self.selected_id)  # initialize relative index
            bond_neighbors = self.current_site.connecting_bonds()
            # site_neighbors = self.get_connected_sites(self.current_site, bond_neighbors)

            # # making the cluster sizes zero before merging. START <<
            bond_gids = self.get_bond_gids(bond_neighbors)
            for bb in bond_gids:
                self.cluster_sizes[bb] = 0
            # # END >>

            bond_neighbors_unique = self.uniqe_gid_bond_neighbors(bond_neighbors)
            merged_cluster_index = self.merge_clusters_v3(bond_neighbors_unique)

            ## Update cluster size. START <<
            self.cluster_sizes[merged_cluster_index] = self.cluster_pool_ref.get_cluster_site_count(merged_cluster_index)
            ## END >>

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
