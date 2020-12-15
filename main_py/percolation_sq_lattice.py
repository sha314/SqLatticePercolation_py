from main_py import lattice
from main_py import cluster
import random
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
        old_relative_index = self.lattice_ref.get_site_by_id(central_site_id).get_relative_index()
        # new_relative_index = self.lattice_ref.get_site_by_id(new_site_id).get_relative_index()
        # print(old_relative_index, " old_relative_index type ", type(old_relative_index))
        new_relative_index = old_relative_index + idx
        # print("new_relative_index type ", type(new_relative_index))
        # print("new_relative_index type ", type(RelativeIndex(index=new_relative_index)))
        return RelativeIndex(index=new_relative_index)

    def get_change_in_relative_index(self, old_relative_index, new_relative_index):
        change = new_relative_index - old_relative_index
        print("get_change_in_relative_index. type of change ", type(change))
        print(change)
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
        pass

    def get_neighbor_site(self, central_id, connecting_bond_id):
        # central_id = current_site.get_id()
        # print("central site id : ", central_id)

        sb2 = self.lattice_ref.get_neighbor_sites(connecting_bond_id)
        connected_sites = sb2.copy()
        print("connected ", connected_sites)
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

    def place_one_site(self):
        print("place_one_site. count ", self.current_idx)
        if self.current_idx >= self.lattice_ref.site_count:
            print("No sites to occupy")
            return False
        self.selected_id = self.site_ids_indices[self.current_idx]
        self.current_site = self.lattice_ref.get_site_by_id(self.selected_id)
        print("selected site ", self.current_site.get_index(), " id ", self.current_site.get_id())
        self.lattice_ref.init_relative_index(self.selected_id)  # initialize relative index
        bond_neighbors = self.current_site.connecting_bonds()
        # site_neighbors = self.get_connected_sites(self.current_site, bond_neighbors)
        
        merged_cluster_index = self.merge_clusters_v2(bond_neighbors)
        # self.lattice_ref.set_site_gid_by_id(selected_id, merged_cluster_index)
        # self.cluster_pool_ref.add_sites(merged_cluster_index, selected_id)
        self.current_idx += 1
        return True

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
        print("root cluster is ", root_clstr)
        for bb in bond_gids:
            if bb == root_clstr:
                # print("bb ", bb, " is a root cluster")
                continue
            # print("merging ", bb, " to ", root_clstr)
            self.cluster_pool_ref.merge_cluster_with(root_clstr, bb, self.lattice_ref)
            pass

        return root_clstr
        pass

    def merge_clusters_v2(self, bond_neighbors):
        """
        merging with relabeling relative indices
        """
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
        print("root cluster is ", root_clstr)
        print("Assign and relabel currently selected site")
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
                    rri = self.get_relative_index(neighbor_site, self.selected_id)
                    self.lattice_ref.set_relative_index(self.selected_id, rri)
                else:
                    print("does not belong to any cluster yet")
                continue
                pass
            pass
        pass
        print("Relabel all cluster according to root cluster and selected site")
        for bb in bond_neighbors:
            bbg = self.lattice_ref.get_bond_by_id(bb).get_gid()
            if bbg == root_clstr:

                continue
            print("relabeling relative index of cluster ", bbg)
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
            return
        old_relative_idx = self.lattice_ref.get_site_by_id(neighbor_site).get_relative_index()
        new_relative_idx = self.get_relative_index(central_site, neighbor_site)
        # if the BBB lines are commented then it sould not affect the result. so why extra lines
        # self.lattice_ref.set_relative_index(neighbor_site, new_relative_idx)  # BBB

        # then relabel all sites belonging to the cluster according to the neighbor
        if self.lattice_ref.get_site_gid_by_id(central_site) >= 0:
            # old_relative_index = self.get_relative_index(central_site, self.selected_id)
            change = self.get_change_in_relative_index(old_relative_idx, new_relative_idx)
            print("change ", change)
            # print("old_relative_index ", old_relative_index)
            for ss in sites_to_relabel:
                # if ss == neighbor_site:  # BBB
                #     print("already got relabeled") # BBB
                #     continue # BBB
                ss_relative_index = self.lattice_ref.get_site_by_id(ss).get_relative_index()
                # change = self.get_change_in_relative_index(old_relative_index, ss_relative_index)
                # print("change ", change)
                print("new_relative_index type ", type(ss_relative_index))
                print("relative index before : ", ss_relative_index)
                ss_relative_index = ss_relative_index + change
                ss_relative_index = RelativeIndex(index=ss_relative_index)
                print("relative index after  : ", ss_relative_index)
                # print("new_relative_index ", new_relative_index)
                self.lattice_ref.get_site_by_id(ss).set_relative_index(ss_relative_index)
                pass
            pass

        pass

    def detect_wrapping(self):
        print("detect_wrapping")
        neighbors = self.lattice_ref.get_site_neighbor_of_site(self.selected_id)
        print("neighbors of self.selected_id : ", neighbors)

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
        sq_lattice_p.lattice_ref.print_bonds()
        sq_lattice_p.lattice_ref.print_sites()
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
    sq_lattice_p = SitePercolation(length=5, seed=0)

    sq_lattice_p.viewLattice(3)
    sq_lattice_p.viewCluster()
    while sq_lattice_p.place_one_site():
        # sq_lattice_p.viewLattice(3)
        # sq_lattice_p.viewLattice(4)
        sq_lattice_p.lattice_ref.print_bonds()
        # sq_lattice_p.detect_wrapping()
        continue
    sq_lattice_p.place_one_site()
    sq_lattice_p.viewLattice(3)
    sq_lattice_p.viewLattice(4)
    sq_lattice_p.viewLattice(1)
    sq_lattice_p.viewCluster()
    pass
