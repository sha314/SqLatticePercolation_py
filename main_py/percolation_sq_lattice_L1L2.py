from main_py import lattice
from main_py import cluster
import random
import math
from main_py.index import *
import gc

from main_py.percolation_sq_lattice import SitePercolation
from main_py.percolation_sq_lattice_L0 import SitePercolationL0

Lattice = lattice.Lattice
ClusterPool = cluster.ClusterPool


class SitePercolationL1(SitePercolationL0):
    def __init__(self, **kwargs):
        super(SitePercolationL1, self).__init__(**kwargs)
        self.signature = super(SitePercolationL1, self).get_signature()
        self.signature += "L1_"

        self.x_occupied = 0
        pass

    def reset(self):
        super(SitePercolationL1, self).reset()
        self.site_ids_indices = list(range(0, self.lattice_ref.length ** 2))
        self.x_occupied = 0

    def get_signature(self):
        return self.signature

    def occupied_summary(self):
        print("SitePercolationL1.occupied_summary")
        print("  1st neighor selected ", self.x_occupied, " times")

    def get_four_neighbor_sites(self, central):
        bonds = self.lattice_ref.get_neighbor_bonds(central)
        sites = []
        for bb in bonds:
            tmp = self.lattice_ref.get_neighbor_sites(bb)
            sites += tmp
            pass
        for ss in sites:
            if ss == central:
                sites.remove(ss)
                pass
        #
        # sites.remove(central)
        print(central, " has four neighbor sites : ", sites)
        return sites

    def select_site(self):
        print("SitePercolationL1.select_site")
        if self.current_idx >= self.lattice_ref.site_count:
            # print("No sites to occupy")
            return False
        rnd = random.randint(self.current_idx, len(self.site_ids_indices) - 1)
        central_X = self.site_ids_indices[rnd]
        if self.lattice_ref.get_site_by_id(central_X).is_occupied():
            print("X is occupied")
            self.x_occupied += 1
            self.lattice_ref.get_site_by_id(central_X).reduce_1st_nn()
            sites = self.get_four_neighbor_sites(central_X)
            print("four neighbors ", sites)
            central2 = sites[random.randint(0, len(sites)-1)]
            # self.swap_ids(central, central2)

            print("number of usable nn ", self.lattice_ref.get_site_by_id(central_X).get_nn_count())
            if self.lattice_ref.get_site_by_id(central_X).is_removable(1):
                print("is_removable")
                self.site_ids_indices[rnd] = self.site_ids_indices[self.current_idx]

                self.current_idx += 1
                pass
            central_X = central2

            pass
        self.selected_id = central_X

        self.current_site = self.lattice_ref.get_site_by_id(self.selected_id)
        print("selected id ", self.selected_id)

        return True



    # def place_one_site(self):
    #     subtract_entropy(root_a, root_b);
    #     auto
    #     root = mergeClusters(root_a, root_b);
    #     add_entropy(root);
    #     track_largest_cluster(root);
    #     track_cluster_count(root_a, root_b);


    pass


class SitePercolationL2(SitePercolationL0):
    def __init__(self, **kwargs):
        super(SitePercolationL2, self).__init__(**kwargs)
        self.signature = super(SitePercolationL2, self).get_signature()
        self.signature += "L2_"
        self.x_occupied = 0
        self.y_occupied = 0
        pass

    def reset(self):
        super(SitePercolationL2, self).reset()
        self.site_ids_indices = list(range(0, self.lattice_ref.length ** 2))
        self.x_occupied = 0
        self.y_occupied = 0

    def get_signature(self):
        return self.signature

    def occupied_summary(self):
        print("SitePercolationL2.occupied_summary")
        print("  1st neighor selected ", self.x_occupied, " times")
        print("  2nd neighor selected ", self.y_occupied, " times")

    def get_four_neighbor_sites(self, central):
        bonds = self.lattice_ref.get_neighbor_bonds(central)
        sites = []
        for bb in bonds:
            tmp = self.lattice_ref.get_neighbor_sites(bb)
            sites += tmp
            pass
        for ss in sites:
            if ss == central:
                sites.remove(ss)
                pass
        #
        # sites.remove(central)
        print(central, " has four neighbor sites : ", sites)
        return sites

    def correct_index_for_periodicity(self, index):
        row = index.row() % self.lattice_ref.length
        column = index.column() % self.lattice_ref.length
        return Index(row, column)

    def select_site(self):
        print("SitePercolationL2.select_site")
        if self.current_idx >= self.lattice_ref.site_count:
            # print("No sites to occupy")
            return False
        rnd = random.randint(self.current_idx, len(self.site_ids_indices) - 1)
        central_X = self.site_ids_indices[rnd]
        central = central_X
        if self.lattice_ref.get_site_by_id(central_X).is_occupied():
            sites = self.get_four_neighbor_sites(central_X)
            Y = sites[random.randint(0, len(sites) - 1)]
            central = Y
            print("X is occupied")
            self.x_occupied += 1
            self.lattice_ref.get_site_by_id(central_X).reduce_1st_nn()
            if self.lattice_ref.get_site_by_id(Y).is_occupied():
                print("Y is occupied")
                self.y_occupied += 1
                self.lattice_ref.get_site_by_id(central_X).reduce_2st_directional_nn()
                # if central2 is occupied then select the one in the direction
                X_index = self.lattice_ref.get_site_by_id(central_X).get_index()
                Y_index = self.lattice_ref.get_site_by_id(Y).get_index()
                delta_X = Y_index - X_index
                delta_X.normalize()
                print(delta_X, " delta X = Y - X => Y ", Y_index, " - ", X_index)
                Z_index = Y_index + delta_X
                print("Z_index ", Z_index)
                Z_index = self.correct_index_for_periodicity(Z_index)
                print("Z_index ", Z_index)
                if self.lattice_ref.get_site_by_id(central_X).is_removable(2):
                    print("is_removable")
                    self.site_ids_indices[rnd] = self.site_ids_indices[self.current_idx]

                    self.current_idx += 1
                    pass
                central = self.lattice_ref.get_site_by_index(Z_index).get_id()

            pass
        # self.swap_ids(central_X, central)
        print("central ", central)
        self.selected_id = central
        self.current_site = self.lattice_ref.get_site_by_id(self.selected_id)
        print("selected id ", self.selected_id)
        return True



    # def place_one_site(self):
    #     subtract_entropy(root_a, root_b);
    #     auto
    #     root = mergeClusters(root_a, root_b);
    #     add_entropy(root);
    #     track_largest_cluster(root);
    #     track_cluster_count(root_a, root_b);


    pass



def test_L1():
    # take arguments from commandline
    sq_lattice_p = SitePercolationL1(length=6, seed=0)
    # sq_lattice_p.viewCluster()
    # sq_lattice_p.viewLattice(1)

    while sq_lattice_p.place_one_site():
        sq_lattice_p.occupied_summary()
        continue
    # sq_lattice_p.occupied_summary()

    sq_lattice_p.viewLattice(1)
    sq_lattice_p.viewCluster()



    pass

def test_L2():
    # take arguments from commandline
    sq_lattice_p = SitePercolationL2(length=6, seed=0)
    # sq_lattice_p.viewCluster()
    # sq_lattice_p.viewLattice(1)

    while sq_lattice_p.place_one_site():
        continue

    sq_lattice_p.occupied_summary()

    sq_lattice_p.viewLattice(1)
    sq_lattice_p.viewCluster()

