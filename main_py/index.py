
class RelativeIndex:
    """
    To find the wrapping cluster we need to use the relative index of sites.

    Upper Left corner is <0,0>
    <y,x> means relative index
    90 degree Clockwise rotated Coordinate system
        y value increases as we go rightward
        x value increases as we go downward

    """
    def __init__(self, x_rel=-1, y_rel=-1):
        self.x_coord = x_rel
        self.y_coord = y_rel
        pass

    def __str__(self):
        return "<{},{}>".format(self.x_coord, self.y_coord)

    def __add__(self, other):
        x_coord = self.x_coord + other.x_coord
        y_coord = self.y_coord + other.y_coord
        return x_coord, y_coord
    pass

class Index:
    def __init__(self, row=-1, col=-1):
        self._row = row
        self._col = col
        pass

    def __sub__(self, other):
        del_row = self._row - other._row
        del_col = self._col - other._col
        return del_row, del_col

    # def __rsub__(self, other):
    #     return self.__sub__(other)

    def row(self):
        return self._row

    def column(self):
        return self._col

    def __str__(self):
        return "({},{})".format(self._row, self._col)
    pass


if __name__ == '__main__':
    oldA = Index(2, 3)
    newA = Index(5, 7)
    print(newA - oldA)
    newA -= oldA
    print(newA)
