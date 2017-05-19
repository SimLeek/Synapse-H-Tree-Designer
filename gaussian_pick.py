import random as r
from scipy.stats import norm
from rtree import index

r.seed(1392781243)

'''percent_within_lower_bound = .2  # less than 25% because of corners'''


'''class LowProbabilityError(Exception):
    pass'''


class ArrayFullError(Exception):
    pass


def generate_neuron_input_points(center_x, center_y, sigma_x, sigma_y, max_width, max_height, num_synapses):
    """Creates a gaussian distribution of points that a neuron can get input from, limited to rectangular bounds."""
    # Use 2 r-trees, create all 8 points surrounding inserted point, search for nearest open spot on collision fail.

    assert (center_x >= 0 and center_x < max_width)
    assert (center_y >= 0 and center_y < max_height)

    '''x_percent_within = norm(center_x, sigma_x).cdf(max_width) - norm(center_x, sigma_x).cdf(0)
    y_percent_within = norm(center_y, sigma_y).cdf(max_height) - norm(center_y, sigma_y).cdf(0)
    if x_percent_within * y_percent_within > percent_within_lower_bound:
        raise LowProbabilityError(
            str(percent_within_lower_bound * 100) + '% of generated points will be out of bounds,'
                                                    ' generating failed cycles.')'''
    # Whoops. The points will actually end up going everywhere except the center.

    idx_inserted = index.Index()
    idx_open = index.Index()

    def insert(bbox):
        pt_x = bbox[0]
        pt_y = bbox[1]

        # insert
        idx_inserted.insert(0, bbox)

        # create open spots
        bbox_u = (pt_x, max(pt_y - 1, 0), pt_x, max(pt_y - 1, 0))
        bbox_d = (pt_x, min(pt_y + 1, max_height), pt_x, min(pt_y + 1, max_height))
        bbox_l = (max(pt_x - 1, 0), pt_y, max(pt_x - 1, 0), pt_y)
        bbox_r = (min(pt_x + 1, max_height), pt_y, min(pt_x + 1, max_height), pt_y)
        bbox_ul = (max(pt_x - 1, 0), max(pt_y - 1, 0), max(pt_x - 1, 0), max(pt_y - 1, 0))
        bbox_dl = (max(pt_x - 1, 0), min(pt_y + 1, max_height), max(pt_x - 1, 0), min(pt_y + 1, max_height))
        bbox_ur = (min(pt_x + 1, max_height), pt_y, min(pt_x + 1, max_height), pt_y)
        bbox_dr = (
            min(pt_x + 1, max_height), min(pt_y + 1, max_height), min(pt_x + 1, max_height), min(pt_y + 1, max_height))

        # add open spots around inserted location
        if len(list(idx_inserted.intersection(bbox_u))) == 0 \
                and len(list(idx_open.intersection(bbox_u))) == 0 \
                and bbox_u != bbox:
            idx_open.insert(int(max_width*bbox_u[1]+bbox_u[0]), bbox_u)
        if len(list(idx_inserted.intersection(bbox_d))) == 0 \
                and len(list(idx_open.intersection(bbox_d))) == 0 \
                and bbox_d != bbox:
            idx_open.insert(int(max_width*bbox_d[1]+bbox_d[0]), bbox_d)
        if len(list(idx_inserted.intersection(bbox_l))) == 0 \
                and len(list(idx_open.intersection(bbox_l))) == 0 \
                and bbox_l != bbox:
            idx_open.insert(int(max_width*bbox_l[1]+bbox_l[0]), bbox_l)
        if len(list(idx_inserted.intersection(bbox_r))) == 0 \
                and len(list(idx_open.intersection(bbox_r))) == 0 \
                and bbox_r != bbox:
            idx_open.insert(int(max_width*bbox_r[1]+bbox_r[0]), bbox_r)
        if len(list(idx_inserted.intersection(bbox_ul))) == 0 \
                and len(list(idx_open.intersection(bbox_ul))) == 0 \
                and bbox_ul != bbox:
            idx_open.insert(int(max_width*bbox_ul[1]+bbox_ul[0]), bbox_ul)
        if len(list(idx_inserted.intersection(bbox_dl))) == 0 \
                and len(list(idx_open.intersection(bbox_dl))) == 0 \
                and bbox_dl != bbox:
            idx_open.insert(int(max_width*bbox_dl[1]+bbox_dl[0]), bbox_dl)
        if len(list(idx_inserted.intersection(bbox_ur))) == 0 \
                and len(list(idx_open.intersection(bbox_ur))) == 0 \
                and bbox_ur != bbox:
            idx_open.insert(int(max_width*bbox_ur[1]+bbox_ur[0]), bbox_ur)
        if len(list(idx_inserted.intersection(bbox_dr))) == 0 \
                and len(list(idx_open.intersection(bbox_dr))) == 0 \
                and bbox_dr != bbox:
            idx_open.insert(int(max_width*bbox_dr[1]+bbox_dr[0]), bbox_dr)

        # un-open inserted location
        if len(list(idx_open.intersection(bbox))) != 0:
            idx_open.delete(max_width*bbox[1]+bbox[0], bbox)

    input_points = []
    for i in range(num_synapses):

        pt_x = min(max_width, max(0, r.gauss(center_x, sigma_x)))
        pt_y = min(max_height, max(0, r.gauss(center_y, sigma_y)))

        bbox = (pt_x, pt_y, pt_x, pt_y)

        if len(list(idx_inserted.intersection(bbox))) == 0:  # point is free
            insert(bbox)
        else:  # point is taken
            nearest_open = list(idx_open.nearest(bbox))
            if len(nearest_open)==0:
                raise ArrayFullError("There are no more places to insert input points.")
            elif len(nearest_open)>1:
                chosen = r.choice(nearest_open)
            else:
                chosen = nearest_open[0]
            bbox = (int(chosen % max_width), int(chosen / max_width), int(chosen % max_width), int(chosen / max_width))
            insert(bbox)

        input_points.append((pt_x, pt_y))

    return input_points
