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

    def place_one_site(self):
        print("place_one_site")
        if self.current_idx >= self.lattice_ref.site_count:
            print("No sites to occupy")
            return False
        selected_id = self.site_ids_indices[self.current_idx]
        site = self.lattice_ref.get_site_by_id(selected_id)
        print("selected site ", site)
        bond_neighbors = site.connecting_bonds()
        bond_gids = self.get_bond_gids(bond_neighbors)
        merged_cluster_index = self.merge_clusters(bond_gids)
        self.lattice_ref.set_site_gid_by_id(selected_id, merged_cluster_index)
        self.cluster_pool_ref.add_sites(merged_cluster_index, selected_id)
        self.current_idx += 1
        return True

    def merge_clusters(self, bond_neighbors):
        print("merging clusters ", bond_neighbors)
        ref_sz = 0
        root_clstr = 0
        for bb in bond_neighbors:
            sz = self.cluster_pool_ref.get_cluster_bond_count(bb)
            if sz >= ref_sz:
                root_clstr = bb
                ref_sz = sz
                pass
            pass
        print("root cluster is ", root_clstr)
        for bb in bond_neighbors:
            if bb == root_clstr:
                print("bb ", bb, " is a root cluster")
                continue
            print("merging ", bb, " to ", root_clstr)
            self.cluster_pool_ref.merge_cluster_with(root_clstr, bb, self.lattice_ref)
            pass

        return root_clstr
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
    sq_lattice_p.viewCluster()
