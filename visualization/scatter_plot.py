import matplotlib.pyplot as plt

def show_scatter(input_points, color='k', area=1):
    x = [p[0] for p in input_points]
    y = [p[1] for p in input_points]

    plt.scatter(x,y,s=area,c=color)
    plt.show()