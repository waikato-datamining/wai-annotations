import numpy as np
from skimage import measure
import cv2
import math


def mask_to_polygon(mask, mask_threshold=0.1, mask_nth=1, view=None, view_margin=5, fully_connected='low'):
    """
    Determines the contour of the object in the mask.
    Uses skimage.measure.find_contours to achieve this:
    https://scikit-image.org/docs/0.8.0/api/skimage.measure.find_contours.html

    :param mask: the numpy matrix with probabilities (0-1) representing the mask
    :type mask: np.array
    :param mask_threshold: the (lower) probability threshold for mask values in order to be considered part of the
                           object (0-1)
    :type mask_threshold: float
    :param mask_nth: the contour tracing can be slow for large masks, by using only every nth row/col, this
                     can be sped up dramatically
    :type mask_nth: int
    :param view: the view of the mask to use in order to speed up polygon calculation, e.g., a bounding box
                 (x0, y0, x1, y1), with x1/y1 being included
    :type view: tuple
    :param view_margin: the margin in pixels to enlarge the view with in each direction
    :type view_margin: int
    :param fully_connected: whether regions of high or low values should be fully-connected at isthmuses
    :type fully_connected: str
    :return: the polygon(s) describing the detected object(s): each contour is an ndarray of shape (n, 2),
             consisting of n (x, y) coordinates along the contour
    :rtype: np.ndarray
    """

    if mask_nth > 1:
        rows = np.array(range(0, mask.shape[0], mask_nth))
        cols = np.array(range(0, mask.shape[1], mask_nth))
        act_mask = mask[np.ix_(rows, cols)]
    else:
        act_mask = mask

    x0 = None
    y0 = None
    if view is not None:
        x0 = max(0, int(math.floor(view[0])) - view_margin)
        y0 = max(0, int(math.floor(view[1])) - view_margin)
        x1 = min(act_mask.shape[1], int(math.ceil(view[2])) + view_margin)
        y1 = min(act_mask.shape[0], int(math.ceil(view[3])) + view_margin)
        view_mask = act_mask[slice(y0,y1+1,1), slice(x0,x1+1,1)]
        act_mask = view_mask

    polys = measure.find_contours(act_mask, mask_threshold, fully_connected)

    if mask_nth > 1:
        for poly in polys:
            for i, p in enumerate(poly):
                poly[i] = p*mask_nth

    if x0 is not None:
        for poly in polys:
            for i, p in enumerate(poly):
                poly[i, 0] += y0
                poly[i, 1] += x0

    return polys


def polygon_to_minrect(poly):
    """
    Determines the minimal rectangle around the provided polygon.
    Uses OpenCV's cv2.minAreaRect method for this.
    http://opencvpython.blogspot.com/2012/06/contours-2-brotherhood.html

    :param poly: the polygon describing a detected object: each contour is an ndarray of shape (n, 2),
                 consisting of n (x, y) coordinates along the contour
    :param poly: np.ndarray
    :return: the minimal rectangle, a tuple of width and height
    :rtype: tuple
    """

    rect = cv2.minAreaRect(np.float32(poly))
    w = rect[1][0]
    h = rect[1][1]
    return w, h


def polygon_to_lists(poly, swap_x_y=False, normalize=False, img_width=1, img_height=1, as_string=False):
    """
    Turns a polygon into two lists, one with xs and one with ys. Coordinates can be normalized.

    :param poly: the polygon to process, array of (x,y) pairs
    :type poly: np.ndarray
    :param swap_x_y: whether to swap x and y
    :type swap_x_y: bool
    :param normalize: whether to return normalized coordinates (requires image width and height parameters)
    :type normalize: bool
    :param img_width: the image width to use for normalizing the coordinates
    :type img_width: int
    :param img_height: the image height to use for normalizing the coordinates
    :type img_height: int
    :param as_string: whether to return the values as string or float
    :type as_string: bool
    :return: tuple of one list containing all xs and one containing all ys
    :rtype: tuple
    """

    px = []
    py = []

    for p in poly:
        if swap_x_y:
            x = p[1]
            y = p[0]
        else:
            x = p[0]
            y = p[1]
        if normalize:
            x = x / img_width
            y = y / img_height
        if as_string:
            x = str(x)
            y = str(y)
        px.append(x)
        py.append(y)

    return px, py
