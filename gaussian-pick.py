import random as r
from rtree import index

r.seed(1392781243)

def generate_neuron_input_points(center_x, center_y, sigma_x, sigma_y, max_width, max_height, num_synapses):
    """Creates a gaussian distribution of points that a neuron can get input from, limited to rectangular bounds."""
    #todo: warn on large sigmas, as they'll cause many repeated loops, and error when max_height/width is 0
    #todo: can't pick same points, need to use a-star algorithm to find nearest open space
    # Use b-tree, start with all open spots as points in b-tree, search for nearest open spot on collision fail

    input_points = []
    for i in range(num_synapses):

        pt_x = min(max_width,max(0,r.gauss(center_x, sigma_x)))
        pt_y = min(max_height,max(0,r.gauss(center_y, sigma_y)))

        input_points.append((pt_x, pt_y))

    return input_points

