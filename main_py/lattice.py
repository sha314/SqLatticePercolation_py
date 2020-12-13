from main_py.site import Site
from main_py.bond import Bond


class Lattice:
    def __init__(self, length):
        self.length = length
        self.bond_count = 2*length**2
        self.site_count = length ** 2
        self.site_matrix = [0] * length**2
        self.site_ids = range(0, length**2)
        self.bond_ids = range(0, 2*length ** 2)
        self.bond_matrix = [0] * 2 * length ** 2
        self.init_lattice()
        self.init_ids()
        pass

    def reset(self):

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
        # print("self.bond_matrix ", self.bond_matrix)
        pass

    def bottom_bond_of_site(self, s0_index):
        return s0_index + self.site_count
        pass

    def top_bond_of_site(self, s0_index):
        """
        top index of a site 'm' is the bottom index of some other site 'n'.
        n = (m + 2*L*L - L) (mod L*L)
        """
        of_bottom_site = (s0_index+self.bond_count-self.length)%self.site_count
        return self.bottom_bond_of_site(of_bottom_site)
        pass

    def right_bond_of_site(self, s0_index):
        return s0_index

    def left_bond_of_site(self, s0_index):
        """
        left index of a site 'm' is the right index of some other site 'n'.
        n =
        """
        col, row = self.get_row_col_from_id(s0_index)
        left_site = row*self.length + (col + self.length - 1) % self.length
        # print("left of ", s0_index, " is the right of ", left_site)
        return self.right_bond_of_site(left_site)

    def get_row_col_from_id(self, s0_index):
        row = s0_index // self.length
        col = s0_index % self.length
        return col, row

    def find_neighbor_bonds(self, s0_index):
        right_bond = self.right_bond_of_site(s0_index)
        # bottom_bond = s0_index + self.site_count
        bottom_bond = self.bottom_bond_of_site(s0_index)
        # left_bond = (s0_index + self.length - 1) % self.length
        left_bond = self.left_bond_of_site(s0_index)
        # top_bond = (s0_index+self.bond_count-self.length)%self.site_count + self.site_count
        top_bond = self.top_bond_of_site(s0_index)
        return [right_bond, bottom_bond, left_bond, top_bond]
        pass

    def get_neighbor_bonds(self, s0_index):
        return self.site_matrix[s0_index].connecting_bonds()
        pass

    def get_neighbor_sites(self, b0_index):
        return self.bond_matrix[b0_index].connected_sites()

    def init_ids(self):
        for rr in range(self.length):
            for cc in range(self.length):
                s0_index = rr*self.length + cc
                bonds = self.find_neighbor_bonds(s0_index)
                self.site_matrix[s0_index].add_connecting_bond(bonds)
                for bb in bonds:
                    self.bond_matrix[bb].add_connected_site(s0_index)
                    pass
                # self.site_matrix[s0_index].add_connecting_bond(right_bond)
                # self.site_matrix[s0_index].add_connecting_bond(bottom_bond)
                # self.site_matrix[s0_index].add_connecting_bond(left_bond)
                # self.site_matrix[s0_index].add_connecting_bond(top_bond)
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
        # print("id ", id)
        self.bond_matrix[id].set_gid(gid)
        pass

    def get_site_gid_by_id(self, id):
        return self.site_matrix[id].get_gid()
        pass

    def get_bond_gid_by_id(self, id):
        # print("id ", id)
        return self.bond_matrix[id].get_gid()
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
        print("<--VIEW BEGIN-->")
        self.print_row_separator(34)
        for rr in range(self.length):
            a = self.get_row_str(rr, formatt)
            print(a)
            b = self.get_row_v_str(rr, formatt)
            print(b)
            self.print_row_separator(34)
            pass
        print("<--VIEW END-->")
        pass

    def view_relative_index(self):
        print("Upper Left corner is <0,0>")
        print("<x,y> means relative index")
        print("90 degree Clockwise rotated Coordinate system")
        print("y value increases as we go rightward. Like columns")
        print("x value increases as we go downward . Like rows")
        print("Format 'gid<x,y>'")
        print("<--Relative index - VIEW BEGIN-->")
        self.print_row_separator(12)
        print("{:>5}".format("|"), end="")
        for cc in range(self.length):
            print("{:6}{:>4}".format(cc, "|"), end="")
            pass
        print()
        self.print_row_separator(12)
        for rr in range(self.length):
            print("{:3} |".format(rr), end="")
            for cc in range(self.length):
                s_index = rr * self.length + cc
                site_s = self.site_matrix[s_index]
                a = site_s.relative_index
                print("{:2}".format(site_s.get_gid()), a, end='|')
                # print("{:7}".foramt(a), end=' |')
                pass
            print()
            pass
        self.print_row_separator(12)
        print("<--Relative index - VIEW END-->")
        pass

    def print_row_separator(self, str_sz=10):
        str_str = ""
        for i in range(str_sz):
            str_str += "-"
            pass
        for cc in range(self.length):
            print(str_str, end='')
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

    def init_relative_index(self, id):
        s_index = self.site_ids[id]
        self.site_matrix[s_index].init_relative_index()
        pass

    def set_relative_index(self, id, relative_index):
        s_index = self.site_ids[id]
        self.site_matrix[s_index].set_relative_index(relative_index)
        pass
    pass


def test(length):
    lattice = Lattice(length)
    lattice.view(0)
    lattice.view(1)
    lattice.view(2)
    # print(lattice.get_row_str(0))


def test_neighbors(length):
    lattice = Lattice(length)
    # lattice.view(0)
    lattice.view(1)
    # lattice.view(2)

    print(lattice.get_neighbor_bonds(0))
    print(lattice.get_neighbor_bonds(2))
    print(lattice.get_neighbor_bonds(5))
    print(lattice.get_neighbor_bonds(13))
    print(lattice.get_neighbor_bonds(19))
    print(lattice.get_neighbor_sites(5))
    print(lattice.get_neighbor_sites(8))
    print(lattice.get_neighbor_sites(50))

    # print(lattice.get_row_str(0))