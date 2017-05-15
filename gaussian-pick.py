import random as r

r.seed(1392781243)

def generate_neuron_input_points(center_x, center_y, sigma_x, sigma_y, max_width, max_height, num_synapses):
    """Creates a gaussian distribution of points that a neuron can get input from, limited to rectangular bounds."""
    #todo: warn on large sigmas, as they'll cause many repeated loops, and error when max_height/width is 0
    input_points = []
    for i in range(num_synapses):

        pt_x = None
        while True: #only accept values within bounds, but don't simply limit as that'll put a lot of points on the edge
            pt_x = min(max_width,max(0,r.gauss(center_x, sigma_x)))
            if 0 < pt_x < max_width:
                break

        pt_y = None
        while True: #only accept values within bounds, but don't simply limit as that'll put a lot of points on the edge
            pt_y = min(max_height,max(0,r.gauss(center_y, sigma_y)))
            if 0 < pt_y < max_height:
                break

        input_points.append((pt_x, pt_y))

    return input_points

