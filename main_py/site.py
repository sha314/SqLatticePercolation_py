from main_py.element import Element
from main_py.index import RelativeIndex
from main_py.index import Index

class Site(Element):
    def __init__(self, row, col):
        super(Site, self).__init__()
        self.classname = "Site"
        # self.row = row
        # self.col = col
        self.connecting_bond_ids = []
        self.index = Index(row=row, col=col)
        self.relative_index = RelativeIndex()
        self.first_nn_count = 4 # for L1 percolation
        self.second_directional_nn_count = 4 # for L2 percolation

    def __str__(self):
        # if self.g_id is not None:
        #     return self.get_str(1)
        # elif self.id is not None:
        #     return self.get_str(2)
        # else:
        #     return self.get_str(0)
        return self.get_str(0)

    def get_nn_count(self):
        return self.first_nn_count, self.second_directional_nn_count

    def reduce_1st_nn(self):
        if self.first_nn_count <=0:
            return
        self.first_nn_count -= 1

    def reduce_2st_directional_nn(self):
        if self.second_directional_nn_count <=0:
            return
        self.second_directional_nn_count -= 1

    def is_removable(self, type=0):
        if type == 1:
            return self.first_nn_count == 0
        elif type == 2:
            return self.second_directional_nn_count == 0
        else:
            return False

    def get_index(self):
        # return self.row, self.col
        return self.index
    pass

    def get_gid(self):
        return self.g_id

    def is_occupied(self):
        return self.g_id >= 0

    def get_id(self):
        return self.id

    def get_str(self, formatt=0):
        if formatt == 1:
            return "({:^5}, {:^5})".format(self.g_id, self.id)
        elif formatt == 2:
            return "{:^5}({:^5},{:^5})".format(self.id, self.index.row(), self.index.column())
            pass
        else:
            # print("row col")
            return "({:^5},{:^5})".format(self.index.row(), self.index.column())
        pass

    def add_connecting_bond(self, bond_id):
        if len(self.connecting_bond_ids) >= 4:
            print("A site connects only four bonds")
            return

        if type(bond_id) is list:
            if len(bond_id) == 4:
                self.connecting_bond_ids += bond_id
                # print("site ", self.id, " got bonds ", bond_id)
                pass
            pass
        else:
            # print("site ", self.id, " got bond ", bond_id)
            self.connecting_bond_ids.append(bond_id)

    def connecting_bonds(self):
        return self.connecting_bond_ids

    def init_relative_index(self):
        self.relative_index = RelativeIndex(0, 0)
        pass

    def get_relative_index(self):
        return self.relative_index

    def set_relative_index(self, r_index):
        self.relative_index = r_index
        pass

    def is_root(self):
        return self.relative_index.row() == 0 and self.relative_index.column() == 0



