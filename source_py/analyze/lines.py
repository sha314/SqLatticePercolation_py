import numpy as np


def draw_vertical_line_at(xval, yrange=(0, 1), size=100):
    """

    @param xval:
    @param yrange:
    @param size:
    @return:
    """
    yy = np.linspace(yrange[0], yrange[1], size)
    xx = xval * np.ones(size)
    return xx, yy


def draw_horizontal_line_at(yval, xrange=(), size=100):
    """

    @param yval:
    @param xrange:
    @param size:
    @return:
    """
    xx = np.linspace(xrange[0], xrange[1], size)
    yy = yval * np.ones(size)
    return xx, yy


def find_intersection(line1, line2, col=None):
    if col is None:
        x1 = line1
        x2 = line2
    else:
        x1 = line1[:, col]
        x2 = line2[:, col]
        pass
    #     print(x1)
    #     print(x2)
    difference = x1 - x2
    #     print(diference)
    dx = np.diff(np.sign(difference))
    idx = np.argmax(np.abs(dx))
    return idx


def find_intersection_and_plot(line1, line2, col=None, ax=None):
    if col is None:
        x1 = line1
        x2 = line2
    else:
        x1 = line1[:, col]
        x2 = line2[:, col]
        pass
    #     print(x1)
    #     print(x2)
    difference = x1 - x2
    sz = difference.shape[0]
    ii = np.arange(sz)
    #     plt.plot(ii, difference)
    ax.plot(ii, np.sign(difference))
    #     print(diference)
    dx = np.diff(np.sign(difference))
    ax.plot(ii[1:], dx)

    idx = np.argmax(np.abs(dx))
    return idx
