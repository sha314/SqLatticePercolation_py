
class OneCluster:
    def __init__(self):
        """
        `id` of the cluster will allow us to isolate one particular cluster in `ClusterPool`
        `gid` of the cluster is the `gid` of all sites and bonds in it.
        """
        self.site_ids = []
        self.bond_ids = []
        self.gid = -1
        self.id = -1
        pass

    def __str__(self):
        ret_str = "[{}] (gid {}): {} sites and {} bonds"
        ret_str = ret_str.format(self.id, self.gid, len(self.site_ids), len(self.bond_ids))
        return ret_str

    def is_empty(self):
        if len(self.site_ids) == 0 and len(self.bond_ids) == 0:
            return True
        return False

    def set_id(self, id):
        """
        `id` of the cluster will allow us to isolate one particular cluster in `ClusterPool`
        :param id:
        :return:
        """
        self.id = id

    def set_gid(self, gid):
        """
        `gid` of the cluster is the `gid` of all sites and bonds in it.
        :param gid:
        :return:
        """
        # print("set_gid ", gid)
        self.gid = gid
        # print("set_gid ", self.gid)

    def get_id(self):
        return self.id

    def get_gid(self):
        return self.gid

    def add_sites(self, site_ids):
        if type(site_ids) is list:
            self.site_ids += site_ids
            pass
        else:
            self.site_ids.append(site_ids)
            pass
        pass

    def add_bonds(self, bond_ids):
        if type(bond_ids) is list:
            self.bond_ids += bond_ids
            pass
        else:
            self.bond_ids.append(bond_ids)
        pass

    def get_bond_count(self):
        return len(self.bond_ids)

    def get_site_count(self):
        return len(self.site_ids)

    def clear(self):
        self.site_ids = []
        self.bond_ids = []
        self.gid = -1
        self.id = -1
        pass

    def view(self):
        if self.is_empty():
            return 0
        print("cluster [", self.id, "] (gid ", self.gid, ") :{")
        print("  sites ({}) ".format(len(self.site_ids)), self.site_ids)
        print("  bonds ({}) ".format(len(self.bond_ids)), self.bond_ids)
        print("}")
        return 1


class ClusterPool:
    """
    List of clusters
    """
    def __init__(self):
        self.cluster_list = []
        self.cluster_id=0
        pass

    def reset(self):

        pass

    def get_cluster_bond_count(self, id):
        return self.cluster_list[id].get_bond_count()

    def get_cluster_site_count(self, id):
        return self.cluster_list[id].get_site_count()

    def create_new_cluster(self, site_ids=[], bond_ids=[], lattice_ref=None):
        # print("method : create_new_cluster")
        clsstr = OneCluster()
        clsstr.add_sites(site_ids)
        clsstr.add_bonds(bond_ids)
        # print("setting gid ")
        clsstr.set_gid(self.cluster_id)
        clsstr.set_id(self.cluster_id)
        # print("bond_ids ", bond_ids)
        for ss in site_ids:
            lattice_ref.set_site_gid_by_id(ss, self.cluster_id) # re assign group id
            pass
        for bb in bond_ids:
            lattice_ref.set_bond_gid_by_id(bb, self.cluster_id) # re assign group id
            pass
        self.cluster_id += 1
        # print("clsstr ")
        # print(clsstr)
        self.cluster_list.append(clsstr)
        pass

    def add_sites(self, index, site_ids):
        self.cluster_list[index].add_sites(site_ids)
        pass

    def add_bonds(self, index, bond_ids):
        self.cluster_list[index].add_bonds(bond_ids)
        pass
    def get_cluster(self, cluster_id):
        if cluster_id >= len(self.cluster_list):
            print("Cluster does not exists")
            return None
        return self.cluster_list[cluster_id]

    def clear_cluster(self, cluster_id):
        self.cluster_list[cluster_id].clear()
        pass

    def merge_cluster_with(self, cluster_A_id, cluster_B_id, lattice_ref):
        """

        :param cluster_A_id:  the cluster. group id of cluster A will persist.
        :param cluster_B_id:  the other cluster that will be merged to this cluster
        :param lattice_ref:   so that it gid of sites and bonds can be modified here
        :return:
        """
        gid = self.cluster_list[cluster_A_id].get_gid()
        print("cluster ", cluster_A_id, " gid ", gid)
        for bb in self.cluster_list[cluster_B_id].bond_ids:
            lattice_ref.set_bond_gid_by_id(bb, gid)
            pass
        for ss in self.cluster_list[cluster_B_id].site_ids:
            print("todo: site ", ss, " gid => ", gid)
            lattice_ref.set_site_gid_by_id(ss, gid)
            tmp = lattice_ref.get_site_by_id(ss).get_gid()
            print("done: site ", ss, " gid => ", tmp)
            pass
        self.cluster_list[cluster_A_id].bond_ids += self.cluster_list[cluster_B_id].bond_ids
        self.cluster_list[cluster_A_id].site_ids += self.cluster_list[cluster_B_id].site_ids
        # self.cluster_list[cluster_B_id].clear()


        pass

    def view(self, view_mode=0):
        """

        :param view_mode: 0 -> simple
                          1 -> extended
        :return:
        """
        print("View cluster < BEGIN")
        # print("self.cluster_list ", self.cluster_list)
        counter = 0
        for clstr in self.cluster_list:
            # print("clstr ", clstr)
            counter += clstr.view()
            pass
        print("\n View cluster END >")
        print("Number of clusters ", counter)
        pass

