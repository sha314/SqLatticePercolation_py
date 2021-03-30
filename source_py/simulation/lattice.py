from source_py.simulation.site import Site
from source_py.simulation.bond import Bond
from source_py.simulation.index import Index

class Lattice:
    def __init__(self, length):
        self.length = length
        self.bond_count = 2*length**2
        self.site_count = length ** 2
        self.site_matrix = [0] * self.site_count
        self.site_ids = range(0, self.site_count)
        self.bond_ids = range(0, self.bond_count)
        self.bond_matrix = [0] * self.bond_count
        self.init_lattice()
        self.init_ids()
        pass

    def reset(self):
        for i in range(len(self.site_matrix)):
            self.site_matrix[i].reset()
        for i in range(len(self.bond_matrix)):
            self.bond_matrix[i].reset()
        pass

    def init_lattice(self):
        l_squared = self.length**2
        for rr in range(self.length):
            for cc in range(self.length):
                s_index = rr*self.length + cc
                v_bond_index = s_index+l_squared
                self.site_matrix[s_index] = Site(rr, cc)
                self.site_matrix[s_index].set_id(s_index)

                self.bond_matrix[s_index] = Bond(rr, cc, 0)
                self.bond_matrix[s_index].set_id(s_index)
                self.bond_matrix[v_bond_index] = Bond(rr, cc, 1)
                self.bond_matrix[v_bond_index].set_id(v_bond_index)

                pass
            pass
        # print("self.bond_matrix ", self.bond_matrix)
        pass

    def calculate_id_from_index(self, index):
        index_list = None
        if type(index) is Index:
            index_list = index.as_list()
            pass
        if index_list is None:
            index_list = index
            pass
        multiplier_list = [self.length**k for k in range(len(index_list))]
        multiplier_list.reverse()
        prods = list(map(lambda a,b:a*b, multiplier_list, index_list))
        # print(prods)
        id_calc = sum(prods)
        # print(id_calc)
        return id_calc

    def list_all_sites(self):
        print("id, gid, index, relative_index, connecting_bond_ids")
        for ss in self.site_matrix:
            print(ss.get_id(), " ", ss.get_gid(), " ", ss.get_index(), " ", ss.get_relative_index(), " ", ss.connecting_bonds())
            pass

    def list_all_bonds(self):
        print("id, gid, index, connecting_site_ids")
        for bb in self.bond_matrix:
            print(bb.get_id(), " ", bb.get_gid(), " ", bb.get_index(), " ", bb.connected_sites())
            pass

    def scan_sites(self):
        """
        written for pytest
        """
        for ss in self.site_matrix:
            id = ss.get_id()
            index = ss.get_index()
            id_calc = self.calculate_id_from_index(index)
            assert id == id_calc
            bonds = ss.connecting_bonds()
            assert len(bonds) == 4
            for bb in bonds:
                siteids = self.bond_matrix[bb].connected_sites()
                assert id in siteids
                pass
            pass
            pass
        pass

    def scan_bonds(self):
        """
        written for pytest
        """
        for bb in self.bond_matrix:
            id = bb.get_id()
            index = bb.get_index()
            id_calc = self.calculate_id_from_index(index)
            assert id == id_calc
            sites = bb.connected_sites()
            assert len(sites) == 2
            for ss in sites:
                bondids = self.site_matrix[ss].connecting_bonds()
                assert id in bondids
                pass
            pass
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

    def get_site_neighbor_of_site(self, s0_index):
        # print("get_site_neighbor_of_site : ", s0_index)
        bonds = self.site_matrix[s0_index].connecting_bonds()
        # print("bonds ", bonds)
        out_list = []
        for bb in bonds:
            nn = self.get_neighbor_sites(bb).copy()
            # print("nn ", nn)
            nn.remove(s0_index)
            out_list.append(nn[0])
            pass
        return out_list

    def get_sites_for_wrapping_test(self, s0_index):
        # print("get_site_neighbor_of_site : ", s0_index)
        central_site = self.site_matrix[s0_index]
        gid_central = central_site.get_gid()
        bonds = central_site.connecting_bonds()
        # print("bonds ", bonds)
        out_list = []
        for bb in bonds:
            nn = self.get_neighbor_sites(bb).copy()
            # print("nn ", nn)
            nn.remove(s0_index)
            gid = self.site_matrix[nn[0]].get_gid()
            if gid == gid_central:
                out_list.append(nn[0])
                pass
            pass
        return out_list

    def print_bonds(self):
        print("print_bonds")
        for i in self.bond_ids:
            bbonds = self.bond_matrix[i]
            c_sites = bbonds.connected_sites()
            if len(c_sites) != 2:
                print("warning : number of connected sites must be 2")
            print("[", i, "] gid=", bbonds.get_gid(), " id=", bbonds.get_id(), " sites=", c_sites)
            pass

    def print_sites(self):
        print("print_sites")
        for i in self.site_ids:
            ssite = self.site_matrix[i]
            c_bonds = ssite.connecting_bonds()
            if len(c_bonds) != 4:
                print("warning : number of connecting bonds must be 4")
            print("[", i, "] gid=", ssite.get_gid(), " id=", ssite.get_id(), " sites=", c_bonds)
            pass

    def init_ids(self):
        for rr in range(self.length):
            for cc in range(self.length):
                s0_index = rr*self.length + cc
                bonds = self.find_neighbor_bonds(s0_index)
                assert len(bonds) == 4
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

    def get_site_by_index(self, index):
        if type(index) is Index:
            # print("got Index ")
            pass
        s0_index = index.row() * self.length + index.column()
        return self.site_matrix[s0_index]
        pass

    def get_id_from_index(self, row, col):
        s0_index = row * self.length + col
        return s0_index

    def get_site_gid_by_index(self, index):
        if type(index) is Index:
            # print("got Index ")
            pass
        s0_index = index.row() * self.length + index.column()
        return self.site_matrix[s0_index].get_gid()
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
        return self.bond_matrix[s0_index]
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
        row_unit_str = 14
        self.print_row_separator(row_unit_str)
        print("{:>5}".format("|"), end="")
        for cc in range(self.length):
            print("{:<6}{:>7}".format(cc, "|"), end="")
            pass
        print()
        self.print_row_separator(row_unit_str)
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
        self.print_row_separator(row_unit_str)
        print("<--Relative index - VIEW END-->")
        pass

    def view_site_gids(self):
        print("Upper Left corner is <0,0>")
        print("<x,y> means relative index")
        print("90 degree Clockwise rotated Coordinate system")
        print("y value increases as we go rightward. Like columns")
        print("x value increases as we go downward . Like rows")
        print("Format 'gid<x,y>'")
        print("<--Relative index - VIEW BEGIN-->")
        row_unit_str = 5
        self.print_row_separator(row_unit_str)
        print("{:>5}".format("|"), end="")
        for cc in range(self.length):
            print("{:<3}{:>1}".format(cc, "|"), end="")
            pass
        print()
        self.print_row_separator(row_unit_str)
        for rr in range(self.length):
            print("{:3} |".format(rr), end="")
            for cc in range(self.length):
                s_index = rr * self.length + cc
                site_s = self.site_matrix[s_index]
                a = site_s.relative_index
                print("{:3}".format(site_s.get_gid()), end='|')
                # print("{:7}".foramt(a), end=' |')
                pass
            print()
            pass
        self.print_row_separator(row_unit_str)
        print("<--Relative index - VIEW END-->")
        pass
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

    def get_all_neighbor_sites(self, central_site_id):
        bonds = self.get_neighbor_bonds(central_site_id)
        four_neighbors = []
        for bid in bonds:
            connected_sites = self.get_neighbor_sites(bid)
            tmp = connected_sites.copy()
            if len(tmp) != 2:
                print("func:get_all_neighbor_sites -> len(connected_sites) != 1")
                print(self.get_bond_by_id(bid))
                pass
            # print("connected_sites ", tmp)
            tmp.remove(central_site_id)

            four_neighbors.append(tmp[0])
            pass
        assert len(four_neighbors) == 4

        return four_neighbors

    def distance_btn_sites(self, site1, site2):
        index1 = site1
        index2 = site2
        if type(site1) is Site:
            index1 = site1.get_index()
        if type(site2) is Site:
            index2 = site2.get_index()
            pass
        d_row = abs(index1.row() - index2.row())
        if d_row == (self.length - 1):
            d_row = 1
        # print("d_row ", d_row)
        # print("d_row % L ", d_row % (self.length - 1))
        d_col = abs(index1.column() - index2.column())
        if d_col == (self.length - 1):
            d_col = 1
        return d_row, d_col

    def test_neighbor_count(self):
        for ss in self.site_matrix:
            bb = set(ss.connecting_bonds())
            assert len(bb) == 4
            pass
        for bb in self.bond_matrix:
            ss = bb.connected_sites()
            if len(ss) < 2:
                print(bb, " bond has ", ss, " sites ")
            assert len(ss) == 2

    def test_lattice(self, gid):
        # for unit test. When the percolation is complete
        # print("test_lattice")
        for ss in self.site_matrix:
            ss.test_site()
            assert ss.get_gid() == gid
            pass
        for bb in self.bond_matrix:
            bb.test_bond()
            assert bb.get_gid() == gid
            pass
        pass

    def test_relative_index(self):

        for site_central in self.site_matrix:
            # print("central site ", site_central, " neighbors {")
            gid_c = site_central.get_gid()
            if gid_c < 0:
                continue
            central_rel_index = site_central.get_relative_index()
            four_neibhbors = self.get_all_neighbor_sites(site_central.get_id())
            column_wise, row_wise = False, False
            active_neighbor_count = 0
            for nbors in four_neibhbors:
                site = self.get_site_by_id(nbors)
                # print(site, end=",")
                gid = site.get_gid()
                if gid < 0:
                    continue
                active_neighbor_count += 1
                relidx = site.get_relative_index()
                dx = central_rel_index.x_coord() - relidx.x_coord()
                dy = central_rel_index.y_coord() - relidx.y_coord()
                if (abs(dy) == 1) or (abs(dy) == (self.length - 1)):
                    column_wise = True
                    pass
                elif (abs(dx) == 1) or (abs(dx) == (self.length - 1)):
                    row_wise = True
                    pass
                if column_wise or row_wise:
                    break
                pass
            # print("}")
            # print("active_neighbor_count ", active_neighbor_count)
            if active_neighbor_count > 0:
                # print("made to assertion")
                assert column_wise or row_wise
            pass

    def test_rwo_col_scan(self):
        ## difference between consecutive x or y values of the relative indices should be either 1 or (L-1)
        # test relative index
        site_prev = None
        site = None
        print("column scan")
        for rr in range(self.length):
            site_prev = None
            for cc in range(self.length):
                idx = rr * self.length + cc
                site = self.get_site_by_id(idx)
                gid1 = site.get_gid()
                if gid1 < 0:
                    site_prev = None
                    continue
                if site_prev is None:
                    site_prev = site
                    continue
                gid0 = site_prev.get_gid()
                if gid1 == gid0 and gid0 >= 0 and gid1 >= 0:
                    prev_relative_index = site_prev.get_relative_index()
                    relative_index = site.get_relative_index()
                    dx = prev_relative_index.x_coord() - relative_index.x_coord()
                    dy = prev_relative_index.y_coord() - relative_index.y_coord()
                    print(prev_relative_index, " - ", relative_index)

                    assert (abs(dy) == 1) or (abs(dy) == (self.length - 1))
                    # assert abs(dx) == 0
                    pass
                site_prev = site
                pass
            pass
        # print("row scan")
        # for cc in range(self.length):
        #     site_prev = None
        #     for rr in range(self.length):
        #         idx = rr * self.length + cc
        #         site = self.get_site_by_id(idx)
        #         if site_prev is None:
        #             site_prev = site
        #             continue
        #             pass
        #         gid1, gid0 = site.get_gid(), site_prev.get_gid()
        #         print(site)
        #         print(site_prev)
        #         if gid1 == gid0 and gid0 >= 0 and gid1 >= 0:
        #
        #             prev_relative_index = site_prev.get_relative_index()
        #             relative_index = site.get_relative_index()
        #             dx = prev_relative_index.x_coord() - relative_index.x_coord()
        #             dy = prev_relative_index.y_coord() - relative_index.y_coord()
        #             print(prev_relative_index, " - ", relative_index)
        #
        #             assert (abs(dx) == 1) or (abs(dx) == (self.length - 1))
        #             # assert abs(dy) == 0
        #             pass
        #         site_prev = site
        #
        #         pass
            pass
        pass
    pass


# def test(length):
#     lattice = Lattice(length)
#     lattice.view(0)
#     lattice.view(1)
#     lattice.view(2)
#     # print(lattice.get_row_str(0))
#
#
def mTest_neighbors():
    length = 5
    lattice = Lattice(length)
    lattice.view(0)
    lattice.view(1)
    lattice.view(2)

    lattice.list_all_sites()
    lattice.list_all_bonds()
    pass
