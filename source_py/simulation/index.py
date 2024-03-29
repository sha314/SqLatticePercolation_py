


class Index:
    def __init__(self, row=-1, col=-1):
        if type(row) is not int:
            print("warning : row index is not integer")
            row = int(row)
            pass
        if type(col) is not int:
            print("warning : col index is not integer")
            col = int(col)
            pass
        self.component_1 = row
        self.component_2 = col
        pass

    def __sub__(self, other):
        del_row = self.component_1 - other.component_1
        del_col = self.component_2 - other.component_2
        return Index(del_row, del_col)

    def __add__(self, other):
        # print("self ", self)
        # print("other ", other)
        component_1 = self.component_1 + other.component_1
        component_2 = self.component_2 + other.component_2
        return Index(component_1, component_2)
    # def __rsub__(self, other):
    #     return self.__sub__(other)

    def row(self):
        return self.component_1

    def column(self):
        return self.component_2

    def as_list(self):
        return self.component_1, self.component_2

    def normalize(self):
        if (self.component_1 == 0) and (self.component_2 != 0):
            self.component_2 = self.component_2 // abs(self.component_2)
        elif (self.component_1 != 0) and (self.component_2 == 0):
            self.component_1 = self.component_1 // abs(self.component_1)
        else:
            # print("Normalization will give float or NAN")
            pass
        pass

    def __str__(self):
        return "({:3},{:3})".format(self.component_1, self.component_2)
    pass

class RelativeIndex(Index):
    """
    To find the wrapping cluster we need to use the relative index of sites.

    Upper Left corner is <0,0>
    <y,x> means relative index
    90 degree Clockwise rotated Coordinate system
        y value increases as we go rightward
        x value increases as we go downward

    """
    def __init__(self, x_rel=0, y_rel=0, index=None):
        if index is None:
            super().__init__(x_rel, y_rel)
            pass
        elif type(index) is Index:
            super().__init__(index.component_1, index.component_2)
            pass
        elif type(index) is RelativeIndex:
            super().__init__(index.component_1, index.component_2)
            pass
        else:
            print("Wrong type. RelativeIndex")
            pass
        # self.x_coord = x_rel
        # self.y_coord = y_rel

    def x_coord(self):
        return self.component_1

    def y_coord(self):
        return self.component_2

    def __str__(self):
        return "<{:3},{:3}>".format(self.component_1, self.component_2)

    def __sub__(self, other):
        """
        subtraction of relative index
        """
        # print("RelativeIndex.__sub__")
        del_row = self.component_1 - other.component_1
        del_col = self.component_2 - other.component_2
        # if abs(del_row) > 1 and del_col == 0:
        #     # print("vertical_wrapping")
        #     del_row /= -del_row
        #     del_row = int(del_row)
        # if abs(del_col) > 1 and del_row == 0:
        #     # print("horizontal_wrapping")
        #     del_col /= -del_col
        #     del_col = int(del_col)
        # if abs(del_row) > 1 and abs(del_col) > 1:
        #     print("both row and column delta cannot be greater than 1 at the same time")
        #     pass
        return RelativeIndex(del_row, del_col)


    pass


if __name__ == '__main__':
    oldA = Index(2, 3)
    newA = Index(5, 7)
    rnewA = RelativeIndex(5, 7)
    print(newA - oldA)
    newA -= oldA
    print(newA)
    print(type(newA))
    print(oldA - rnewA)
    print(RelativeIndex(index=oldA))
