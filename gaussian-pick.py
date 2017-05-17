import random as r
from rtree import index

r.seed(1392781243)

def generate_neuron_input_points(center_x, center_y, sigma_x, sigma_y, max_width, max_height, num_synapses):
    """Creates a gaussian distribution of points that a neuron can get input from, limited to rectangular bounds."""
    #todo: warn on large sigmas, as they'll cause many repeated loops, and error when max_height/width is 0
    #todo: can't pick same points, need to use a-star algorithm to find nearest open space
    # Breadth first search is the best method to fix this, with the goal being any open space,
    #  and building and keeping the shortest path tree
    #  with the nearest open space overriding other goals for each point
    #  Also, store the goal point as it's own class and add points in b-tree to that class when they say it's their goal
    #   and move points bordering 8 others (2D) in same class to non-bordering index group in b-tree
    #   because when that open space goal disappears, the points bordering those can be selected for and
    #   the new nearest goal can be calculated from those neighbors and cascaded down into the group

    input_points = []
    for i in range(num_synapses):

        pt_x = min(max_width,max(0,r.gauss(center_x, sigma_x)))
        pt_y = min(max_height,max(0,r.gauss(center_y, sigma_y)))

        input_points.append((pt_x, pt_y))

    return input_points

