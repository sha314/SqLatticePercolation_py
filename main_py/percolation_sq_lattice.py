from main_py import lattice
from main_py import cluster
import random

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
        if formatt >= 3:
            self.lattice_ref.view_relative_index()
            pass
        else:
            self.lattice_ref.view(formatt)
        pass

    def viewCluster(self):
        self.cluster_pool_ref.view()
        pass


class SitePercolation(Percolation):
    def __init__(self, **kwargs):
        super(SitePercolation, self).__init__(**kwargs)
        self.init_clusters()
        self.site_ids_indices = list(range(0, self.lattice_ref.length**2))
        self.current_idx = 0
        self.shuffle()
        self.current_site = None
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
        print("place_one_site")
        if self.current_idx >= self.lattice_ref.site_count:
            print("No sites to occupy")
            return False
        selected_id = self.site_ids_indices[self.current_idx]
        self.current_site = self.lattice_ref.get_site_by_id(selected_id)
        print("selected site ", self.current_site)
        self.lattice_ref.init_relative_index(selected_id)  # initialize relative index
        bond_neighbors = self.current_site.connecting_bonds()
        site_neighbors = self.get_connected_sites(self.current_site, bond_neighbors)
        
        merged_cluster_index = self.merge_clusters(site_neighbors, bond_neighbors)
        self.lattice_ref.set_site_gid_by_id(selected_id, merged_cluster_index)
        self.cluster_pool_ref.add_sites(merged_cluster_index, selected_id)
        self.current_idx += 1
        return True

    def merge_clusters(self, site_neighbors, bond_neighbors):
        bond_gids = self.get_bond_gids(bond_neighbors)
        print("merging clusters ", bond_gids)
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
                print("bb ", bb, " is a root cluster")
                continue
            print("merging ", bb, " to ", root_clstr)
            self.cluster_pool_ref.merge_cluster_with(root_clstr, bb, self.lattice_ref)
            pass

        return root_clstr
        pass

    def get_relative_index(self, old_site_id, new_site_id):
        old_index = self.lattice_ref.get_site_by_id(old_site_id).get_index()
        new_index = self.lattice_ref.get_site_by_id(new_site_id).get_index()
        del_r, del_c = new_index - old_index
        old_relative_index = self.lattice_ref.get_site_by_id(old_site_id).get_relative_index()
        pass

    def get_bond_gids(self, bond_ids):
        gids = set()
        for bb in bond_ids:
            gid = self.lattice_ref.get_bond_by_id(bb).get_gid()
            gids.add(gid)
        return list(gids)


class BondPercolation(Percolation):
    def __init__(self, **kwargs):
        super(BondPercolation, self).__init__(**kwargs)
        pass


def test_site_percolation():
    sq_lattice_p = SitePercolation(length=5, seed=0)
    sq_lattice_p.viewCluster()
    sq_lattice_p.viewLattice(1)

    sq_lattice_p.place_one_site()

    sq_lattice_p.viewLattice(1)
    sq_lattice_p.viewCluster()

    sq_lattice_p.place_one_site()

    sq_lattice_p.viewLattice(1)
    # sq_lattice_p.viewCluster()

    sq_lattice_p.place_one_site()

    sq_lattice_p.viewLattice(1)
    # sq_lattice_p.viewCluster()
    while sq_lattice_p.place_one_site():
        continue
    sq_lattice_p.viewLattice(1)
    sq_lattice_p.viewLattice(2)
    sq_lattice_p.viewLattice(0)
    sq_lattice_p.viewCluster()

def test_relative_index():
    # take arguments from commandline
    sq_lattice_p = SitePercolation(length=5, seed=0)
    # sq_lattice_p.viewCluster()
    sq_lattice_p.viewLattice(1)

    sq_lattice_p.place_one_site()
    # sq_lattice_p.viewLattice(1)
    # sq_lattice_p.viewLattice(3)

    sq_lattice_p.place_one_site()
    # sq_lattice_p.viewLattice(1)
    # sq_lattice_p.viewLattice(3)

    sq_lattice_p.place_one_site()
    # sq_lattice_p.viewLattice(1)
    # sq_lattice_p.viewLattice(3)

    sq_lattice_p.place_one_site()
    sq_lattice_p.viewLattice(1)
    sq_lattice_p.viewLattice(3)

    sq_lattice_p.place_one_site()
    sq_lattice_p.viewLattice(1)
    sq_lattice_p.viewLattice(3)

    # sq_lattice_p.place_one_site()
    # sq_lattice_p.viewLattice(1)
    # sq_lattice_p.viewLattice(3)
    # sq_lattice_p.viewCluster()

    # sq_lattice_p.place_one_site()

    # sq_lattice_p.viewLattice(1)
    # sq_lattice_p.viewCluster()

    # sq_lattice_p.place_one_site()
    #
    # sq_lattice_p.viewLattice(1)
    # sq_lattice_p.viewCluster()
    # while sq_lattice_p.place_one_site():
    #     continue
    # sq_lattice_p.viewLattice(1)
    # sq_lattice_p.viewCluster()
    pass
