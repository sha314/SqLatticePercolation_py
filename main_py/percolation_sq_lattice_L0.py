from main_py import lattice
from main_py import cluster
import random
import numpy as np

from main_py.percolation_sq_lattice import SitePercolation

Lattice = lattice.Lattice
ClusterPool = cluster.ClusterPool


class SitePercolationL0(SitePercolation):
    def __init__(self, **kwargs):
        super(SitePercolationL0, self).__init__(**kwargs)
        self.signature = super(SitePercolationL0, self).get_signature()
        self.signature += "L0_"
        self.first_run = True
        self.occupation_prob_list = list()
        self.entropy_list = None
        self.order_wrapping_list = None
        self.order_largest_list = None
        pass

    def get_signature(self):
        return self.signature

    def reset(self):
        # n = gc.collect()
        # print("Number of unreachable objects collected by GC:", n)
        # print("Uncollectable garbage:", gc.garbage)
        super(SitePercolationL0, self).reset()
        # if self.first_run:
        #     self.occupation_prob_list = list()
        #     pass
        del self.entropy_list
        self.entropy_list = list()
        del self.order_wrapping_list
        self.order_wrapping_list = list()
        del self.order_largest_list
        self.order_largest_list = list()

    def shuffle(self):
        print("SitePercolationL0:shuffle")
        # print("warning ! shuffle off")
        random.shuffle(self.site_ids_indices)
        for i in range(len(self.site_ids_indices)):
            a = self.site_ids_indices[i]
            self.reverse_ids_indices[a] = i
            pass
        pass

    def swap_ids(self, id1, id2):
        if id1 == id2:
            return -1
        ix1 = self.reverse_ids_indices[id1]
        ix2 = self.reverse_ids_indices[id2]
        self.site_ids_indices[ix1] = id2
        self.site_ids_indices[ix2] = id1
        self.reverse_ids_indices[id2] = ix1
        self.reverse_ids_indices[id1] = ix2

    def get_order_param_wrapping_array(self):
        return self.order_wrapping_list

    def get_order_param_largest_array(self):
        return self.order_largest_list

    def get_entropy_array(self):
        return self.entropy_list

    def get_data_array(self):
        pp = self.get_occupation_prob_array()
        HH = self.get_entropy_array()
        PP1 = self.get_order_param_wrapping_array()
        PP2 = self.get_order_param_largest_array()
        print(len(pp))
        print(len(HH))
        print(len(PP1))
        print(len(PP2))
        return np.c_[pp, HH, PP1, PP2]

    def get_occupation_prob_array(self):
        return self.occupation_prob_list


    def run_once(self):
        # sq_lattice_p.viewLattice(3)
        # sq_lattice_p.viewCluster()
        print("get_occupation_prob_array ", self.get_occupation_prob_array())
        while self.place_one_site():
            print("self.selection_flag ", self.selection_flag)
            if self.selection_flag == 0:
                self.detect_wrapping()
                p = self.occupation_prob()
                # print("p = ", p)
                H = self.entropy()
                P1 = self.order_param_wrapping()
                P2 = self.order_param_largest_clstr()
                if self.first_run:
                    self.occupation_prob_list.append(p)
                    pass
                self.entropy_list.append(H)
                self.order_wrapping_list.append(P1)
                self.order_largest_list.append(P2)

        # if self.first_run:
        #     print("self.first_run")
        #     while self.place_one_site():
        #         self.detect_wrapping()
        #         p = self.occupation_prob()
        #         # print("p = ", p)
        #         H = self.entropy()
        #         P1 = self.order_param_wrapping()
        #         P2 = self.order_param_largest_clstr()
        #         self.occupation_prob_list.append(p)
        #         self.entropy_list.append(H)
        #         self.order_wrapping_list.append(P1)
        #         self.order_largest_list.append(P2)
        #
        #         pass
        # else:
        #     print("not self.first_run")
        #     while self.place_one_site():
        #         self.detect_wrapping()
        #         H = self.entropy()
        #         P1 = self.order_param_wrapping()
        #         P2 = self.order_param_largest_clstr()
        #         self.entropy_list.append(H)
        #         self.order_wrapping_list.append(P1)
        #         self.order_largest_list.append(P2)
        #
        #
        #
        #         pass
        print("get_occupation_prob_array ", self.get_occupation_prob_array())
        self.first_run = False
        pass

    # def place_one_site(self):
    #     subtract_entropy(root_a, root_b);
    #     auto
    #     root = mergeClusters(root_a, root_b);
    #     add_entropy(root);
    #     track_largest_cluster(root);
    #     track_cluster_count(root_a, root_b);


    pass



def test_relative_index():
    # take arguments from commandline
    sq_lattice_p = SitePercolation(length=6, seed=0)
    # sq_lattice_p.viewCluster()
    # sq_lattice_p.viewLattice(1)

    sq_lattice_p.place_one_site()
    # sq_lattice_p.viewLattice(1)
    sq_lattice_p.viewLattice(3)

    sq_lattice_p.place_one_site()
    # sq_lattice_p.viewLattice(1)
    sq_lattice_p.viewLattice(3)

    sq_lattice_p.place_one_site()
    # sq_lattice_p.viewLattice(1)
    sq_lattice_p.viewLattice(3)
    # print("***** THISIS ****")
    sq_lattice_p.place_one_site()
    # sq_lattice_p.viewLattice(1)
    sq_lattice_p.viewLattice(3)

    sq_lattice_p.place_one_site()
    # sq_lattice_p.viewLattice(1)
    sq_lattice_p.viewLattice(3)

    sq_lattice_p.place_one_site()
    # sq_lattice_p.viewLattice(1)
    sq_lattice_p.viewLattice(3)
    # sq_lattice_p.viewCluster()

    sq_lattice_p.place_one_site()
    sq_lattice_p.viewLattice(3)

    sq_lattice_p.place_one_site()
    sq_lattice_p.viewLattice(3)

    sq_lattice_p.place_one_site()
    sq_lattice_p.viewLattice(3)
    #
    sq_lattice_p.place_one_site()
    sq_lattice_p.viewLattice(3)
    # sq_lattice_p.viewLattice(1)
    # sq_lattice_p.viewCluster()

    sq_lattice_p.place_one_site()
    sq_lattice_p.viewLattice(3)

    sq_lattice_p.place_one_site()
    sq_lattice_p.viewLattice(3)
    sq_lattice_p.viewLattice(4)

    sq_lattice_p.place_one_site()
    sq_lattice_p.viewLattice(3)
    sq_lattice_p.viewLattice(4)

    sq_lattice_p.place_one_site()
    sq_lattice_p.viewLattice(3)
    sq_lattice_p.viewLattice(4)

    # sq_lattice_p.place_one_site()
    # sq_lattice_p.viewLattice(3)
    # sq_lattice_p.viewLattice(4)
    #
    # sq_lattice_p.place_one_site()
    # sq_lattice_p.viewLattice(3)
    # sq_lattice_p.viewLattice(4)
    #
    # sq_lattice_p.place_one_site()
    # sq_lattice_p.viewLattice(3)
    # sq_lattice_p.viewLattice(4)
    #
    # sq_lattice_p.viewLattice(3)
    # sq_lattice_p.viewCluster()
    # while sq_lattice_p.place_one_site():
    #     sq_lattice_p.viewLattice(3)
    #     sq_lattice_p.viewLattice(4)
    #     continue
    # sq_lattice_p.place_one_site()
    # sq_lattice_p.viewLattice(3)
    # sq_lattice_p.viewLattice(4)
    # sq_lattice_p.viewLattice(1)
    # sq_lattice_p.viewCluster()
    pass


def test_detect_wrapping():
    # take arguments from commandline
    sq_lattice_p = SitePercolationL0(length=6, seed=18)

    # sq_lattice_p.viewLattice(3)
    # sq_lattice_p.viewCluster()
    i = 0
    while sq_lattice_p.place_one_site():
        print("p= ", sq_lattice_p.occupation_prob(),
              " entropy_v1 ", sq_lattice_p.entropy_v1(),
              " entropy_v2 ", sq_lattice_p.entropy_v2(),
              " order wrapping ",             sq_lattice_p.order_param_wrapping(),
              " order largest ", sq_lattice_p.order_param_largest_clstr())
        # sq_lattice_p.viewLattice(3)
        # sq_lattice_p.viewLattice(4)
        # sq_lattice_p.lattice_ref.print_bonds()
        i += 1
        sq_lattice_p.detect_wrapping()
        # if(sq_lattice_p.detect_wrapping()):
            # print("p= ", sq_lattice_p.occupation_prob(), " entropy ", sq_lattice_p.entropy(), " order ",
            #       sq_lattice_p.order_param_largest_clstr())
            # print("Wrapping detected ***************** <<<")
            # break
        # if i > 2:
        #     break
        continue
        pass
    # sq_lattice_p.viewLattice(3)
    # sq_lattice_p.viewLattice(4)
    # sq_lattice_p.viewLattice(1)
    # sq_lattice_p.viewCluster()
    pass

def test_large(lengthL):
    # take arguments from commandline
    sq_lattice_p = SitePercolationL0(length=lengthL, seed=9)

    # sq_lattice_p.viewLattice(3)
    # sq_lattice_p.viewCluster()
    while sq_lattice_p.place_one_site():
        # print("largest cluster ", sq_lattice_p.largest_cluster())
        # print("p= ", sq_lattice_p.occupation_prob(), " entropy ", sq_lattice_p.entropy(), " order ", sq_lattice_p.order_param())
        # sq_lattice_p.viewLattice(3)
        # sq_lattice_p.viewLattice(4)
        # sq_lattice_p.lattice_ref.print_bonds()
        if(sq_lattice_p.detect_wrapping()):
            print("p= ", sq_lattice_p.occupation_prob(), " entropy ", sq_lattice_p.entropy(), " order ",
                  sq_lattice_p.order_param_largest_clstr())
            print("Wrapping detected  ********** << ")
            break
        continue
    # sq_lattice_p.viewLattice(3)
    # sq_lattice_p.viewLattice(4)
    # sq_lattice_p.viewLattice(1)
    # sq_lattice_p.viewCluster()

    # while sq_lattice_p.place_one_site():
    #     # print("largest cluster ", sq_lattice_p.largest_cluster())
    #     print("entropy ", sq_lattice_p.entropy(), " order ", sq_lattice_p.order_param())
    #     continue
    # sq_lattice_p.viewCluster()
    pass