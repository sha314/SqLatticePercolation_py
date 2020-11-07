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
        selected_id = self.site_ids_indices[self.current_idx]
        site = self.lattice_ref.get_site_by_id(selected_id)
        print(site)
        print(site.connecting_bonds())
        self.current_idx += 1
        pass




class BondPercolation(Percolation):
    def __init__(self, **kwargs):
        super(BondPercolation, self).__init__(**kwargs)
        pass


def test_site_percolation():
    sq_lattice_p = SitePercolation(length=5, seed=0)
    sq_lattice_p.viewCluster()
    sq_lattice_p.viewLattice(1)

    sq_lattice_p.place_one_site()
    # sq_lattice_p.viewLattice()
    # sq_lattice_p.viewCluster()
