from main_py.site import Site
from main_py.bond import Bond


class Lattice:
    def __init__(self, length):
        self.length = length
        self.site_matrix = [0] * length**2
        self.site_ids = range(0, length**2)
        self.bond_ids = range(0, 2*length ** 2)
        self.bond_matrix = [0] * 2 * length ** 2
        self.init_lattice()
        self.init_ids()
        pass

    def init_lattice(self):
        l_squared = self.length**2
        for rr in range(self.length):
            for cc in range(self.length):
                s_index = rr*self.length + cc
                v_bond_index = s_index+l_squared
                self.site_matrix[s_index] = Site(rr, cc)
                self.site_matrix[s_index].set_id(s_index)

                self.bond_matrix[s_index] = Bond(rr, cc)
                self.bond_matrix[s_index].set_id(s_index)
                self.bond_matrix[v_bond_index] = Bond(rr, cc, 1)
                self.bond_matrix[v_bond_index].set_id(v_bond_index)

                pass
            pass
        print(self.bond_matrix)
        pass

    def init_ids(self):
        for rr in range(self.length):
            for cc in range(self.length):
                s0_index = rr*self.length + cc
                s1_index = rr*self.length + (cc+1) % self.length
                self.site_matrix[s0_index].add_connecting_bond(s0_index)
                self.site_matrix[s1_index].add_connecting_bond(s1_index)
                # v_bond_index = s_index+self.length**2
                # self.site_matrix[s_index] = Site(rr, cc)
                # self.bond_matrix[s_index] = Bond(rr, cc)
                # self.bond_matrix[v_bond_index] = Bond(rr, cc, 1)
                pass
            pass
        pass

    def get_site_by_id(self, id):
        return self.site_matrix[id]
        pass

    def get_bond_by_id(self, id):
        return self.bond_matrix[id]
        pass

    def set_site_gid_by_id(self, id, gid):
        self.site_matrix[id].set_gid(gid)
        pass

    def set_bond_gid_by_id(self, id, gid):
        print("id ", id)
        self.bond_matrix[id].set_gid(gid)
        pass

    def get_site_by_index(self, row, col):
        s0_index = row * self.length + col
        return self.site_matrix[s0_index]
        pass

    def get_bond_by_index(self, row, col, hv_flag=0):
        """

        :param row:
        :param col:
        :param hv_flag: 0 means horizontal and 1 means vertical
        :return:
        """
        if abs(hv_flag) > 1:
            print("invalid hv flag")
            pass
        s0_index = row * self.length + col
        s0_index += hv_flag * self.length**2
        return self.site_matrix[s0_index]
        pass

    def get_site_id_list(self):
        return self.site_ids

    def get_bond_id_list(self):
        return self.bond_ids
        pass

    def view(self, formatt=0):
        print("format : ")
        print("{site}           {horizontal bond}")
        print("{vertical bond}  {               }")
        print("The lattice : ")
        for rr in range(self.length):
            a = self.get_row_str(rr, formatt)
            print(a)
            b = self.get_row_v_str(rr, formatt)
            print(b)
            pass
        print("<--", end='')
        for cc in range(self.length):
            print("---------#---------", end='')
            pass
        print()
        pass

    def get_row_str(self, row, format=0):
        r_string = []
        for cc in range(self.length):
            s_index = row * self.length + cc
            str1 = self.site_matrix[s_index].get_str(format)
            str2 = self.bond_matrix[s_index].get_str(format)
            str0 = ''
            for i in range(len(str2) - len(str1)):
                str0 += ' '
            r_string.append("{}{}  {}".format(str1, str0, str2))
        return r_string

    def get_row_v_str(self, row, format=0):
        r_string = []
        for cc in range(self.length):
            s_index = row * self.length + cc
            v_bond_index = s_index + self.length ** 2
            str3 = self.bond_matrix[v_bond_index].get_str(format)
            str4 = ''
            for i in str3:
                str4 += ' '
                pass
            r_string.append("{}  {}".format(str3, str4))

            pass
        return r_string
    pass


def test(length):
    lattice = Lattice(length)
    lattice.view(0)
    lattice.view(1)
    lattice.view(2)
    # print(lattice.get_row_str(0))