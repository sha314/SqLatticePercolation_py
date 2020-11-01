from main_py.element import Element


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
        self.connected_site_ids.append(site_id)

    def connected_sites(self):
        return self.connected_site_ids


        pass