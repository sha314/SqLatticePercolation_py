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
        self.shortest_path_p = 0
        pass

    def reset(self):
        super(ShortestPathAfter_pc, self).reset()
        self.shortest_path_p = 0

    def get_shortest_path_p(self):
        return self.shortest_path_p

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
            # self.viewLattice(3)
            if self.selection_flag == 0:
                if self.detect_wrapping():
                    # self.viewLattice(3)
                    # scan rows and columns of the current site to find the shortest path of same gid
                    index = self.current_site.get_index()
                    column_flag, row_flag = self.scan_row_col_of_selected_site(index)

                    if column_flag or row_flag:
                        # print("Got to the shortest path point by placing ", self.current_site)
                        # self.viewLattice(1)
                        # self.viewLattice(2)
                        # self.viewLattice(3)
                        self.shortest_path_p = self.occupation_prob()
                        break
                        pass

                    pass


        self.first_run = False
        pass

    def scan_row_col_of_selected_site(self, index):
        rr, cc = index.row(), index.column()
        # print("central site (", rr, ",", cc, ")")
        column_flag = True
        row_flag = True
        for xcx in range(self.lattice_ref.length):

            idx = self.lattice_ref.get_id_from_index(rr, xcx)
            gid = self.lattice_ref.get_site_gid_by_id(idx)
            # scan_str1 = "{}({},{})".format(gid, rr, xcx)

            if gid != self.wrapping_cluster_id:
                column_flag = False
                pass

            idx = self.lattice_ref.get_id_from_index(xcx, cc)
            gid = self.lattice_ref.get_site_gid_by_id(idx)
            # scan_str2 = "{}({},{})".format(gid, xcx, cc)
            # print("    scanning ", scan_str1, " and ", scan_str2)
            if gid != self.wrapping_cluster_id:
                row_flag = False
                pass

            pass
        return column_flag, row_flag



