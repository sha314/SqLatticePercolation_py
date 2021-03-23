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

Lattice = lattice.Lattice
ClusterPool = cluster.ClusterPool


class ShortestPathAfter_pc(SitePercolation):
    def __init__(self, **kwargs):
        super(ShortestPathAfter_pc, self).__init__(**kwargs)

        self.signature = super(ShortestPathAfter_pc, self).get_signature()
        self.signature += "shortest_path_"
        # self.first_run = True
        # self.occupation_prob_list = list()
        # self.entropy_list = None
        # self.order_wrapping_list = None
        # self.order_largest_list = None
        pass

    def get_signature(self):
        return self.signature

    def run_once(self):
        """
        Single realization
        """
        # sq_lattice_p.viewLattice(3)
        # sq_lattice_p.viewCluster()
        # print("get_occupation_prob_array ", self.get_occupation_prob_array())
        while self.place_one_site():
            # print("self.selection_flag ", self.selection_flag)
            if self.selection_flag == 0:
                if self.detect_wrapping():
                    # scan rows and columns of the current site to find the shortest path of same gid
                    index = self.current_site.get_index()
                    rr, cc = index.row(), index.column()
                    flag = True
                    for c in range(self.lattice_ref.length):
                        idx = self.lattice_ref.get_id_from_index(rr, c)
                        gid = self.lattice_ref.get_site_gid_by_id(idx)
                        if gid != self.wrapping_cluster_id:
                            flag = False
                            break
                            pass
                        pass
                    if flag:
                        for r in range(self.lattice_ref.length):
                            idx = self.lattice_ref.get_id_from_index(r, cc)
                            gid = self.lattice_ref.get_site_gid_by_id(idx)
                            if gid != self.wrapping_cluster_id:
                                flag = False
                            pass
                        pass
                    if flag:
                        print("Got to the shortest path point by placing ", self.current_site)
                        # self.viewLattice(1)
                        # self.viewLattice(2)
                        self.viewLattice(3)
                        break
                        pass

                    pass
                # p = self.occupation_prob()
                # # print("p = ", p)
                # H = self.entropy()
                # P1 = self.order_param_wrapping()
                # P2 = self.order_param_largest_clstr()
                # if self.first_run:
                #     self.occupation_prob_list.append(p)
                #     pass
                # self.entropy_list.append(H)
                # self.order_wrapping_list.append(P1)
                # self.order_largest_list.append(P2)

        self.first_run = False
        pass

