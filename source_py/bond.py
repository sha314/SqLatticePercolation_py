from source_py.element import Element


class Bond(Element):
    def __init__(self, row, col, type=0):
        """

        :param row:
        :param col:
        :param type: default 0 for horizontal bond. 1 is for vertical bond
        """
        super(Bond, self).__init__()
        self.classname = "Bond"
        self.row = row
        self.col = col
        self.type = type
        self.connected_site_ids = [] # connected site ids

    def reset(self):
        super(Bond, self).reset()
        # self.connected_site_ids = []
        pass

    def test_bond(self):
        # for unit test
        # print("test_bond")
        assert len(self.connected_site_ids) == 2
        sett = set(self.connected_site_ids)
        assert len(sett) == 2  # repetition
        pass

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
            return "({:^5},{:^5},{})".format(self.row, self.col, 'h' if self.type == 0 else 'v')
        pass

    def add_connected_site(self, site_id):
        if len(self.connected_site_ids) >=2:
            print("A bond connects only two sites")
            return
        if type(site_id) is list:
            if len(site_id) == 2:
                self.connected_site_ids += site_id
                # print("bond ", self.id, " got sites ", site_id)
                pass
            pass
        else:
            # print("bond ", self.id, " got site ", site_id)
            self.connected_site_ids.append(site_id)

    def connected_sites(self):
        return self.connected_site_ids


        pass