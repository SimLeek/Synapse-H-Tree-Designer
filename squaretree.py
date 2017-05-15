import math as m

class TreeSquare(object):
    """
    This will be used to determine the number of overlaps in a spacial input synapse structure so height can be figured.
    
    This class will subclass itself so that it contains enough squares to cover a rectangle.
    
    For rectangels, the squares will start out at the maximum size without exceeding parent bounds, and the remaning 
    area will be kept as another subclass, but the aspect ratio will indicate another rectangle.
    
    For squares, the area will be shared between four equal sized squares.
    
    Once the squares could only contain points, subdivision ends.
    """

    def __init__(self, x, y, width, height, parent=None):
        self.children = []
        self.parent = parent
        self.top_left = (x, y)
        self.x = x
        self.y = y
        self.width, self.height = width, height

        #Since every node in the tree will be used, might as well generate it all at the start if memory can handle it.
        self._generate_tree()
        self.used_spaces = 0

    def get_max_overlap(self):
        """Get the minimum number of layers we'll need to print the neural input synapses."""
        if len(self.children)==0:
            return self.used_spaces
        else:
            max = 0
            for child in self.children:
                temp = child.get_max_overlap()
                if temp > max:
                    max = temp
            return max

    def increment_used_amount(self, amount):
        self.used_spaces += amount

        if self.parent != None:
            self.parent.increment_used_amount(amount)

    def children_by_openness(self):
        """Return sorted children so most open child is first."""
        return sorted(self.children, key=lambda child: child.used_spaces)

    def children_by_z(self):
        """Return sorted children in order of how words would be read from a book."""
        #y just needs to be multiplied by something at least as large as the row length.
        return sorted(self.children, key = lambda  child: child.y*len(self.children)+child.x)

    def children_by_nearness(self, x, y):
        """Return sorted children in order of how close they are to a given point."""
        return sorted(self.children, key = lambda child: m.sqrt((child.x - x)**2 + (child.y - y)**2))

    def _generate_tree(self):
        """Generates all of the nodes beneath this one."""

        square_length = None

        if self.width>1 or self.height>1:
            if self.width != self.height: #rectangular, so break into squares
                if self.width > self.height:

                    square_length = self.height
                    square_width = square_length

                    for i in range(int(m.ceil(self.width/square_length))):

                        if (self.x + square_length*i) > self.x+self.width: #only changes last loop
                            square_width =  square_length*i - self.width

                        self.children.append(
                            TreeSquare(
                                self.x + square_length*i,
                                self.y,
                                square_width,
                                square_length,
                                self
                            )
                        )

                else:
                    square_length = self.width
                    square_height = square_length

                    for i in range(int(m.ceil(self.width / square_length))):

                        if (self.y + square_length * i) > self.y + self.height: #only changes last loop
                            square_height = square_length * i - self.width

                        self.children.append(
                            TreeSquare(
                                self.x + square_length * i,
                                self.y,
                                square_length,
                                square_height,
                                self
                            )
                        )
            else: #square, so break into four sections
                #guaranteed both x and y greater than 1
                self.children.append(
                    TreeSquare(
                        self.x,
                        self.y,
                        int(self.width / 2), #odd vs even fix
                        int(self.height / 2),
                        self
                    )
                )
                self.children.append(
                    TreeSquare(
                        self.x + int(self.width / 2),
                        self.y,
                        self.width - int(self.width / 2),  # odd vs even fix
                        int(self.height / 2),
                        self
                    )
                )
                self.children.append(
                    TreeSquare(
                        self.x,
                        self.y + int(self.height / 2),
                        int(self.width / 2),  # odd vs even fix
                        self.height - int(self.height / 2),
                        self
                    )
                )
                self.children.append(
                    TreeSquare(
                        self.x,
                        self.y,
                        self.width - int(self.width / 2),  # odd vs even fix
                        self.height - int(self.height / 2),
                        self
                    )
                )
