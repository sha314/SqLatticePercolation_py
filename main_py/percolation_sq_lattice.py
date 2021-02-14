from main_py import lattice
from main_py import cluster
import random
import math
import numpy as np
from main_py.index import *

Lattice = lattice.Lattice
ClusterPool = cluster.ClusterPool


class Percolation:
    def __init__(self, **kwargs):
        print("kwargs ", kwargs)
        length = kwargs['length']
        if "seed" in kwargs.keys():
            print("Custom seeding. Testing mode")
            random.seed(kwargs['seed'])
            pass
        self.lattice_ref = Lattice(length)
        self.cluster_pool_ref = ClusterPool()
        pass

    def reset(self):
        self.lattice_ref.reset()
        self.cluster_pool_ref.reset()
        pass

    def viewLattice(self, formatt=0):
        if formatt < 0:
            print("undefined format")
            pass
        elif formatt == 3:
            self.lattice_ref.view_relative_index()
            pass
        elif formatt == 4:
            self.lattice_ref.view_site_gids()
            pass
        else:
            self.lattice_ref.view(formatt)
        pass

    def viewCluster(self):
        self.cluster_pool_ref.view()
        pass

    def get_bond_gids(self, bond_ids):
        gids = set()
        for bb in bond_ids:
            gid = self.lattice_ref.get_bond_by_id(bb).get_gid()
            gids.add(gid)
        return list(gids)

    def get_site_gids(self, site_ids):
        gids = set()
        for ss in site_ids:
            gid = self.lattice_ref.get_site_by_id(ss).get_gid()
            print("site ", ss, " gid => ", gid)
            gids.add(gid)
        return list(gids)
        pass

    def wrapping_correction_relative_index(self, delta_X):
        """
        when delta X of relative indices are greater than 1 and there are in
        the opposite edge of the lattice.
        """
        # LL = self.lattice_ref.length
        xx = delta_X.x_coord()
        yy = delta_X.y_coord()
        if abs(xx) > 1:
            xx = -xx // abs(xx)
            pass
        if abs(yy) > 1:
            yy = -yy // abs(yy)
            pass
        # print(type(xx), " and ", type(yy))
        return RelativeIndex(xx, yy)
        pass

    def get_relative_index(self, central_site_id, neighbor_site_id):
        """
        neighbor_site_id will get a new relative index based on central_site_id. only one condition,
                new site must be a neighbor of old site
        """
        # print("central_site_id ", central_site_id)
        # print("neighbor_site_id ", neighbor_site_id)
        central_index = self.lattice_ref.get_site_by_id(central_site_id).get_index()
        neighbor_index = self.lattice_ref.get_site_by_id(neighbor_site_id).get_index()
        # print("central_index ", central_index)
        # print("neighbor_index ", neighbor_index)
        idx = RelativeIndex(index=neighbor_index) - RelativeIndex(index=central_index)
        # print("idx ", idx)
        idx = self.wrapping_correction_relative_index(idx)
        # print("after wrapping correction ", idx)
        old_relative_index = self.lattice_ref.get_site_by_id(central_site_id).get_relative_index()
        # new_relative_index = self.lattice_ref.get_site_by_id(new_site_id).get_relative_index()
        # print(old_relative_index, " old_relative_index type ", type(old_relative_index))
        new_relative_index = old_relative_index + idx
        # print("new_relative_index type ", type(new_relative_index))
        # print("new_relative_index type ", type(RelativeIndex(index=new_relative_index)))
        return RelativeIndex(index=new_relative_index)

    def get_change_in_relative_index(self, old_relative_index, new_relative_index):
        # print("get_change_in_relative_index")
        # print("old_relative_index - new_relative_index = ", old_relative_index, " - ", new_relative_index)
        change = new_relative_index - old_relative_index
        # print("get_change_in_relative_index. type of change ", type(change))
        # print("change ", change)
        return RelativeIndex(index=change)


class SitePercolation(Percolation):
    def __init__(self, **kwargs):
        super(SitePercolation, self).__init__(**kwargs)
        self.init_clusters()
        self.site_ids_indices = list(range(0, self.lattice_ref.length**2))
        self.current_idx = 0
        self.shuffle()
        self.current_site = None
        self.selected_id = None
        self.cluster_count = self.lattice_ref.bond_count
        self.largest_cluster_sz = 0
        self.largest_cluster_id = 0
        self.entropy_value = 0
        self.after_wrapping = False
        self.wrapping_cluster_id = -1
        pass

    def init_clusters(self):
        for bb in self.lattice_ref.get_bond_id_list():
            self.cluster_pool_ref.create_new_cluster([], [bb], self.lattice_ref)
            pass
        pass

    def shuffle(self):
        random.shuffle(self.site_ids_indices)
        pass

    def reset(self):
        """
        reset for next
        """
        super(SitePercolation, self).reset()
        self.current_idx = 0
        self.shuffle()
        self.after_wrapping = False
        self.wrapping_cluster_id = -1
        pass

    def get_neighbor_site(self, central_id, connecting_bond_id):
        # central_id = current_site.get_id()
        # print("central site id : ", central_id)

        sb2 = self.lattice_ref.get_neighbor_sites(connecting_bond_id)
        connected_sites = sb2.copy()
        # print("connected ", connected_sites)
        connected_sites.remove(central_id)
        if len(connected_sites) != 1:
            print("Number of neighbors must be exactly 1 : get_connected_sites()")
            pass
        # print("neighbor site ids ", neighbor_sites)
        return connected_sites[0]
        pass

    def get_connected_sites(self, site, bond_neighbors):
        # print("central site index : ", site.get_index())
        central_id = site.get_id()
        # print("central site id : ", central_id)
        neighbor_sites = []
        for bb in bond_neighbors:
            sb2 = self.lattice_ref.get_bond_by_id(bb)
            connected_sites = list(sb2.connected_sites())
            # print("connected ", connected_sites)
            connected_sites.remove(central_id)
            if len(connected_sites) > 1:
                print("Number of neighbors cannot exceed 2 : get_connected_sites()")
                pass
            neighbor_sites.append(connected_sites[0])
            pass
        # print("neighbor site ids ", neighbor_sites)
        return neighbor_sites
        pass

    def select_site(self):
        if self.current_idx >= self.lattice_ref.site_count:
            # print("No sites to occupy")
            return False
        self.selected_id = self.site_ids_indices[self.current_idx]
        self.current_site = self.lattice_ref.get_site_by_id(self.selected_id)
        # print("selected id ", self.selected_id)
        return True

    def place_one_site(self):
        # print("************************ place_one_site. count ", self.current_idx)
        flag = self.select_site()
        if flag:

            # print("selected site ", self.current_site.get_index(), " id ", self.current_site.get_id())
            self.lattice_ref.init_relative_index(self.selected_id)  # initialize relative index
            bond_neighbors = self.current_site.connecting_bonds()
            # site_neighbors = self.get_connected_sites(self.current_site, bond_neighbors)

            # self.entropy_substract()

            merged_cluster_index = self.merge_clusters_v2(bond_neighbors)

            self.track_largest_cluster(merged_cluster_index)
            # self.entropy_add(merged_cluster_index)

            # self.lattice_ref.set_site_gid_by_id(selected_id, merged_cluster_index)
            # self.cluster_pool_ref.add_sites(merged_cluster_index, selected_id)
            self.current_idx += 1
            pass
        return flag

    def track_largest_cluster(self, new_cluster):
        new_size = self.cluster_pool_ref.get_cluster_bond_count(new_cluster)
        # self.cluster_pool_ref.get_cluster_site_count(new_cluster)
        if new_size > self.largest_cluster_sz:
            self.largest_cluster_id = new_cluster
            self.largest_cluster_sz = new_size
            pass

        # self.entropy_value = 0

    def entropy_substract(self):

        pass

    def entropy_add(self):

        pass

    def occupation_prob(self):
        return self.current_idx / self.lattice_ref.site_count

    def entropy(self):
        H = 0
        for i in range(self.cluster_count):
            b_count = self.cluster_pool_ref.get_cluster_bond_count(i)
            mu = b_count / self.lattice_ref.bond_count
            if mu == 0:
                # print("empty cluster")
                continue
            log_mu = math.log(mu)
            H += mu*log_mu
            pass
        self.entropy_value = -H
        return self.entropy_value

    def largest_cluster(self):
        return self.largest_cluster_sz

    def order_param_largest_clstr(self):
        return self.largest_cluster_sz / self.lattice_ref.bond_count

    def order_param_wrapping(self):
        if self.after_wrapping:
            # print("wrapping cluster id ", self.wrapping_cluster_id)
            count = self.cluster_pool_ref.get_cluster_bond_count(self.wrapping_cluster_id)
            return count / self.lattice_ref.bond_count
        return 0.
        pass


    def merge_clusters(self, bond_neighbors):
        bond_gids = self.get_bond_gids(bond_neighbors)
        # print("merging clusters ", bond_gids)
        ref_sz = 0
        root_clstr = 0
        for bb in bond_gids:
            sz = self.cluster_pool_ref.get_cluster_bond_count(bb)
            if sz >= ref_sz:
                root_clstr = bb
                ref_sz = sz
                pass
            pass
        # print("root cluster is ", root_clstr)
        for bb in bond_gids:
            if bb == root_clstr:
                # print("bb ", bb, " is a root cluster")
                continue
            # print("merging ", bb, " to ", root_clstr)
            self.cluster_pool_ref.merge_cluster_with(root_clstr, bb, self.lattice_ref)
            pass

        return root_clstr
        pass

    def uniqe_gid_bond_neighbors(self, bond_neighbors):
        gids = []
        unique_bond_ids = []
        for bb in bond_neighbors:
            bbg = self.lattice_ref.get_bond_by_id(bb).get_gid()
            if bbg in gids:
                continue
            else:
                gids.append(bbg)
                unique_bond_ids.append(bb)
                pass
            pass
        return unique_bond_ids

    def merge_clusters_v2(self, bond_neighbors):
        """
        merging with relabeling relative indices
        """
        bond_neighbors = self.uniqe_gid_bond_neighbors(bond_neighbors)
        bond_gids = self.get_bond_gids(bond_neighbors)
        # site_gids = self.get_site_gids(site_neighbors)
        # print("site_gids ", site_gids)
        # print("bond_gids ", bond_gids)
        # print("set minus ", set(site_gids) - set(bond_gids))
        # print("merging clusters ", bond_gids)
        ref_sz = 0
        root_clstr = bond_gids[0]
        for bbg in bond_gids:
            sz = self.cluster_pool_ref.get_cluster_bond_count(bbg)
            if sz >= ref_sz:
                root_clstr = bbg
                ref_sz = sz
                pass
            pass
        # print("root cluster is ", root_clstr)
        # print("Assign and relabel currently selected site")
        for bb in bond_neighbors:
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
        for bb in bond_neighbors:
            bbg = self.lattice_ref.get_bond_by_id(bb).get_gid()
            if bbg == root_clstr:

                continue
            # print("relabeling relative index of cluster ", bbg)
            self.relabel_relative_indices(bb)
            # print("merging ", bbg, " to ", root_clstr)
            self.cluster_pool_ref.merge_cluster_with(root_clstr, bbg, self.lattice_ref)
            pass

        for bbg in bond_gids:
            if bbg == root_clstr:
                # print("bb ", bbg, " is a root cluster")
                continue
            self.cluster_pool_ref.clear_cluster(bbg)

        return root_clstr
        pass

    def relabel_relative_indices(self, connecting_bond):
        bond = self.lattice_ref.get_bond_by_id(connecting_bond)
        bbg = bond.get_gid()
        central_site = self.current_site.get_id()
        neighbor_site = self.get_neighbor_site(central_site, bond.get_id())
        # print("neighbor_site ", neighbor_site)
        sites_to_relabel = self.cluster_pool_ref.get_sites(bbg)
        # print("sites_to_relabel ", sites_to_relabel)
        # relabel neighbor according to central site
        if len(sites_to_relabel) == 0:
            # print("len(sites_to_relabel) == 0 ")
            return
        old_relative_idx = self.lattice_ref.get_site_by_id(neighbor_site).get_relative_index()
        new_relative_idx = self.get_relative_index(central_site, neighbor_site)
        # if the BBB lines are commented then it sould not affect the result. so why extra lines
        # self.lattice_ref.set_relative_index(neighbor_site, new_relative_idx)  # BBB

        # then relabel all sites belonging to the cluster according to the neighbor
        if self.lattice_ref.get_site_gid_by_id(central_site) >= 0:
            # old_relative_index = self.get_relative_index(central_site, self.selected_id)
            change = self.get_change_in_relative_index(old_relative_idx, new_relative_idx)
            # print("change ", change)
            # print("old_relative_index ", old_relative_idx)
            for ss in sites_to_relabel:
                # if ss == neighbor_site:  # BBB
                #     print("already got relabeled") # BBB
                #     continue # BBB
                ss_relative_index = self.lattice_ref.get_site_by_id(ss).get_relative_index()
                # change = self.get_change_in_relative_index(old_relative_index, ss_relative_index)
                # print("change ", change)
                # print("new_relative_index type ", type(ss_relative_index))
                # print("relative index before : ", ss_relative_index)
                ss_relative_index = ss_relative_index + change
                ss_relative_index = RelativeIndex(index=ss_relative_index)
                # print("relative index after  : ", ss_relative_index)
                # print("new_relative_index ", new_relative_index)
                self.lattice_ref.get_site_by_id(ss).set_relative_index(ss_relative_index)
                pass
            pass

        pass

    def detect_wrapping(self):
        if self.after_wrapping:
            return True
        # print("detect_wrapping")
        neighbors = self.lattice_ref.get_sites_for_wrapping_test(self.selected_id)
        # print("neighbors of self.selected_id with same gid : ", neighbors)
        central_r_index = self.current_site.get_relative_index()
        for ss in neighbors:
            rss = self.lattice_ref.get_site_by_id(ss).get_relative_index()
            delta_x = central_r_index.x_coord() - rss.x_coord()
            delta_y = central_r_index.y_coord() - rss.y_coord()
            if (abs(delta_x) > 1) or (abs(delta_y) > 1):
                # print(self.selected_id, " and ", ss, " are connected via wrapping")
                # print("indices are ", self.lattice_ref.get_site_by_id(self.selected_id).get_index(),
                #       " and ", self.lattice_ref.get_site_by_id(ss).get_index())
                # print("relative ", central_r_index, " - ", rss)
                self.after_wrapping = True
                self.wrapping_cluster_id = self.lattice_ref.get_site_by_id(self.selected_id).get_gid()
                return True
            pass
        return False

class SitePercolation_L1(SitePercolation):
    def __init__(self, **kwargs):
        super(SitePercolation_L1, self).__init__(**kwargs)
        self.first_run = True

        self.occupation_prob_list = None
        self.entropy_list = None
        self.order_wrapping_list = None
        self.order_largest_list = None
        pass

    def reset(self):
        super(SitePercolation_L1, self).reset()
        if self.first_run:
            self.occupation_prob_list = list()
            pass
        self.entropy_list = list()
        self.order_wrapping_list = list()
        self.order_largest_list = list()

    def get_entropy_array(self):
        return self.entropy_list

    def get_occupation_prob_array(self):
        return self.occupation_prob_list

    def get_order_param_wrapping_array(self):
        return self.order_wrapping_list

    def get_order_param_largest_array(self):
        return self.order_largest_list

    def get_data_array(self):
        pp = self.get_occupation_prob_array()
        HH = self.get_entropy_array()
        PP1 = self.get_order_param_wrapping_array()
        PP2 = self.get_order_param_largest_array()
        # print(pp)
        # print(HH)
        return np.c_[pp, HH, PP1, PP2]

    def run_once(self):
        # sq_lattice_p.viewLattice(3)
        # sq_lattice_p.viewCluster()
        if self.first_run:
            while self.place_one_site():
                self.detect_wrapping()
                p = self.occupation_prob()
                H = self.entropy()
                P1 = self.order_param_wrapping()
                P2 = self.order_param_largest_clstr()
                self.occupation_prob_list.append(p)
                self.entropy_list.append(H)
                self.order_wrapping_list.append(P1)
                self.order_largest_list.append(P2)

                pass
        else:
            while self.place_one_site():
                self.detect_wrapping()
                H = self.entropy()
                P1 = self.order_param_wrapping()
                P2 = self.order_param_largest_clstr()
                self.entropy_list.append(H)
                self.order_wrapping_list.append(P1)
                self.order_largest_list.append(P2)



                pass
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

class BondPercolation(Percolation):
    def __init__(self, **kwargs):
        super(BondPercolation, self).__init__(**kwargs)
        pass


def test_site_percolation():
    sq_lattice_p = SitePercolation(length=5, seed=0)
    sq_lattice_p.lattice_ref.print_bonds()
    sq_lattice_p.lattice_ref.print_sites()
    sq_lattice_p.viewCluster()
    sq_lattice_p.viewLattice(1)

    # sq_lattice_p.place_one_site()
    #
    # sq_lattice_p.viewLattice(1)
    # sq_lattice_p.viewCluster()
    #
    # sq_lattice_p.place_one_site()
    #
    # sq_lattice_p.viewLattice(1)
    # # sq_lattice_p.viewCluster()
    #
    # sq_lattice_p.place_one_site()
    #
    # sq_lattice_p.viewLattice(1)
    # sq_lattice_p.viewCluster()
    while sq_lattice_p.place_one_site():
        # sq_lattice_p.lattice_ref.print_bonds()
        # sq_lattice_p.lattice_ref.print_sites()
        continue
    sq_lattice_p.viewLattice(1)
    sq_lattice_p.viewLattice(2)
    sq_lattice_p.viewLattice(0)
    sq_lattice_p.viewCluster()

def test_relative_index():
    # take arguments from commandline
    sq_lattice_p = SitePercolation(length=5, seed=0)
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
    sq_lattice_p = SitePercolation(length=6, seed=18)

    # sq_lattice_p.viewLattice(3)
    # sq_lattice_p.viewCluster()
    i = 0
    while sq_lattice_p.place_one_site():
        # print("p= ", sq_lattice_p.occupation_prob(), " entropy ", sq_lattice_p.entropy(), " order ",
        #       sq_lattice_p.order_param())
        # sq_lattice_p.viewLattice(3)
        # sq_lattice_p.viewLattice(4)
        # sq_lattice_p.lattice_ref.print_bonds()
        i += 1
        if(sq_lattice_p.detect_wrapping()):
            print("p= ", sq_lattice_p.occupation_prob(), " entropy ", sq_lattice_p.entropy(), " order ",
                  sq_lattice_p.order_param_largest_clstr())
            print("Wrapping detected ***************** <<<")
            break
        if i > 5:
            break
        continue
    sq_lattice_p.viewLattice(3)
    # sq_lattice_p.viewLattice(4)
    # sq_lattice_p.viewLattice(1)
    # sq_lattice_p.viewCluster()
    pass

def test_large(lengthL):
    # take arguments from commandline
    sq_lattice_p = SitePercolation(length=lengthL, seed=9)

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
