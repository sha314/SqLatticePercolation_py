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

Lattice = lattice.Lattice
ClusterPool = cluster.ClusterPool

class SitePercolation_old_def(SitePercolation):
    def __init__(self, **kwargs):
        super(SitePercolation_old_def, self).__init__(**kwargs)
        self.signature = "SitePercolationOldDef"
        self.max_entropy = math.log(self.lattice_ref.bond_count)
        self.entropy_value = 0
        pass

    def get_cluster_size(self, cluster_id):
        """
        In new definition of site percolation, cluter size id defined by the number of bonds in the cluster.
        Initially all cluster contains exactly 1 bonds.

        Just changing this definition will change the definition of cluster and hence the definition of site percolation itself

        """
        s_count = self.cluster_pool_ref.get_cluster_site_count(cluster_id)
        return s_count

    def order_param_largest_clstr(self):
        return self.largest_cluster_sz / self.lattice_ref.site_count

    def order_param_wrapping(self):
        if self.after_wrapping:
            # print("wrapping cluster id ", self.wrapping_cluster_id)
            # count = self.cluster_pool_ref.get_cluster_bond_count(self.wrapping_cluster_id)
            count = self.get_cluster_size(self.wrapping_cluster_id)
            ret_val = count / self.lattice_ref.site_count
            # print("wrapping cluster size ", count, " P = ", ret_val)
            return ret_val
        return 0.
        pass

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
