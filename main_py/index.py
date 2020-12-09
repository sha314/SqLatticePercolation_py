
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

    pass
    
