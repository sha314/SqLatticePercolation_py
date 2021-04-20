from source_py.simulation import lattice, cluster

from source_py.simulation.percolation_sq_lattice import SitePercolation

Lattice = lattice.Lattice
ClusterPool = cluster.ClusterPool
import logging

class SitePercolationL0(SitePercolation):
    def __init__(self, **kwargs):
        super(SitePercolationL0, self).__init__(**kwargs)
        self.signature = super(SitePercolationL0, self).get_signature()
        self.signature += "L0_"
        # self.first_run = True
        # self.occupation_prob_list = list()
        # self.entropy_list = None
        # self.order_wrapping_list = None
        # self.order_largest_list = None
        # print("SitePercolationL0.init")
        logging.info("SitePercolationL0.init")
        pass

    def get_signature(self):
        return self.signature

    def reset(self):
        # n = gc.collect()
        # print("Number of unreachable objects collected by GC:", n)
        # print("Uncollectable garbage:", gc.garbage)
        super(SitePercolationL0, self).reset()
        # print("current sequence ", self.site_ids_indices)







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
    sq_lattice_p = SitePercolation(length=6, seed=310)
    # sq_lattice_p.viewCluster()
    # sq_lattice_p.viewLattice(1)
    # sq_lattice_p.reset()
    while sq_lattice_p.place_one_site():
        sq_lattice_p.viewLattice(3)
        if sq_lattice_p.detect_wrapping():

            print("Wrapping detected")
        pass
    # # sq_lattice_p.viewLattice(1)
    # sq_lattice_p.viewLattice(3)
    #
    # sq_lattice_p.place_one_site()
    # # sq_lattice_p.viewLattice(1)
    # sq_lattice_p.viewLattice(3)
    #
    # sq_lattice_p.place_one_site()
    # # sq_lattice_p.viewLattice(1)
    # sq_lattice_p.viewLattice(3)
    # # print("***** THISIS ****")
    # sq_lattice_p.place_one_site()
    # # sq_lattice_p.viewLattice(1)
    # sq_lattice_p.viewLattice(3)
    #
    # sq_lattice_p.place_one_site()
    # # sq_lattice_p.viewLattice(1)
    # sq_lattice_p.viewLattice(3)
    #
    # sq_lattice_p.place_one_site()
    # # sq_lattice_p.viewLattice(1)
    # sq_lattice_p.viewLattice(3)
    # # sq_lattice_p.viewCluster()
    #
    # sq_lattice_p.place_one_site()
    # sq_lattice_p.viewLattice(3)
    #
    # sq_lattice_p.place_one_site()
    # sq_lattice_p.viewLattice(3)
    #
    # sq_lattice_p.place_one_site()
    # sq_lattice_p.viewLattice(3)
    # #
    # sq_lattice_p.place_one_site()
    # sq_lattice_p.viewLattice(3)
    # # sq_lattice_p.viewLattice(1)
    # # sq_lattice_p.viewCluster()
    #
    # sq_lattice_p.place_one_site()
    # sq_lattice_p.viewLattice(3)
    #
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


def test_reset_relative_index():
    # take arguments from commandline
    sq_lattice_p = SitePercolation(length=6, seed=41)

    while sq_lattice_p.place_one_site():
        sq_lattice_p.viewLattice(3)
        if sq_lattice_p.detect_wrapping():

            print("Wrapping detected")
        pass

    print("Resetting now ************** <<<<<<<<<<")
    sq_lattice_p.reset()
    while sq_lattice_p.place_one_site():
        sq_lattice_p.viewLattice(3)
        if sq_lattice_p.detect_wrapping():

            print("Wrapping detected")
        pass

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
        if(sq_lattice_p.detect_wrapping()):
            print("p= ", sq_lattice_p.occupation_prob(), " entropy ", sq_lattice_p.entropy(), " order ",
                  sq_lattice_p.order_param_largest_clstr())
            print("Wrapping detected ***************** <<<")
            break
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
