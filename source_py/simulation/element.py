
class Element:
    def __init__(self):
        self.id = None

        self.g_id = -1

    def reset(self):
        # self.id = None
        self.g_id = -1

    def set_id(self, id):
        self.id = id

    def get_id(self):
        return self.id

    def set_gid(self, gid):
        """
        Group id. elements with same g_id belongs to same cluster
        :param gid:
        :return:
        """
        if self.id is None:
            print("!!warning!! id is not set.")
            pass
        self.g_id = gid

    def get_gid(self):
        return self.g_id