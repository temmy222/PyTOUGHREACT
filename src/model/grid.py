class Grid(object):
    def __init__(self, unit_system, grid_type, grid_top):
        self.unit_system = unit_system
        self.grid_type = grid_type
        self.grid_top = grid_top
    
    def add_x_dimension(self, x_array):
        self.x_dimension = x_array

    def add_y_dimension(self, y_array):
        self.y_dimension = y_array

    def add_z_dimension(self, z_array):
        self.z_dimension = z_array

