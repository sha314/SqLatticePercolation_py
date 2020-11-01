from main_py.element import Element


class Site(Element):
    def __init__(self, row, col):
        super(Site, self).__init__()
        self.classname = "Site"
        self.row = row
        self.col = col
        self.connecting_bond_ids = []

    def __str__(self):
        if self.g_id is not None:
            return self.get_str(1)
        elif self.id is not None:
            return self.get_str(2)
        else:
            return self.get_str(0)
        pass

    def get_str(self, formatt=0):
        if formatt == 1:
            return "({:^5}, {:^5})".format(self.g_id, self.id)
        elif formatt == 2:
            return "{:^5}({:^5},{:^5})".format(self.id, self.row, self.col)
            pass
        else:
            return "({:^5},{:^5})".format(self.row, self.col)
        pass

    def add_connecting_bond(self, bond_id):
        if len(self.connecting_bond_ids) >= 4:
            print("A site connects only four bonds")
            return
        self.connecting_bond_ids.append(bond_id)

    def connecting_bonds(self):
        return self.connecting_bond_ids


