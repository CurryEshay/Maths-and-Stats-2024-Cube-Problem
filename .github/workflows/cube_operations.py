class Cube:
    """Class to cubes with all methods"""
    # records all activations done to cube
    cube_history = []
    # dunder methods
    def __init__(self, dimension):
        self.cube = []
        self.dimension = dimension
        # generates all z layers (YX plane) cube
        for layer_z in range(1 , dimension + 1):
            self.cube.append([])
            # generates row in x direction
            for row_y in range(1 , dimension + 1):
                self.cube[layer_z - 1].append([])
                # generates all cells (all y values) in given x row
                for cell_x in range(1, dimension + 1):
                    # adds cell in given (x , y , z) cord
                    self.cube[layer_z - 1][row_y - 1].append(0)

    def __len__(self):
        return len(self.cube)

    def __str__(self):
        return str(self.cube)
    def display_cube(self):
        print(self.cube)
        for layer in range(1, self.dimension + 1):
            print(f'The layer (XY plane) is: {layer}')
            for cell_index in range(1, self.dimension + 1):
                print(self.cube[layer - 1][cell_index - 1])

    def reset_cube(self):
        self.__init__(self.dimension)
        self.history_reset()
    def activate_cell(self, x_cord , y_cord , z_cord):
        # sets the cell itself to active
        self.cube[z_cord - 1][y_cord - 1][x_cord - 1] -= 2
        # sets all cells in z-row to active
        for i in range(1, self.dimension + 1):
            self.cube[i - 1][y_cord - 1][x_cord - 1] += 1
        # sets all cells in y row to be active
        for i in range(1, self.dimension + 1):
            self.cube[z_cord - 1][i - 1][x_cord - 1] += 1
        # sets all cells in x row to be active
        for i in range(1, self.dimension + 1):
            self.cube[z_cord - 1][y_cord - 1][i - 1] += 1
        # add to history
        self.history_add(x_cord, y_cord, z_cord)

    # activates multiple at once
    def list_activate_cells(self, cord_list):
        for cord in cord_list:
            self.activate_cell(int(cord[0]), int(cord[1]), int(cord[2]))

    # de-activates multiple at once
    def list_deactivate_cells(self, cord_list):
        for cord in cord_list:
            self.deactivate_cell(int(cord[0]), int(cord[1]), int(cord[2]))

    def deactivate_cell(self, x_cord , y_cord , z_cord):
        # sets the cell itself to inactive
        self.cube[z_cord - 1][y_cord - 1][x_cord - 1] = 0
        # sets all cells in z-row to in-active
        for i in range(1, self.dimension + 1):
            self.cube[i - 1][y_cord - 1][x_cord - 1] = 0
        # sets all cells in y row to be in-active
        for i in range(1, self.dimension + 1):
            self.cube[z_cord - 1][i - 1][x_cord - 1] = 0
        # sets all cells in x row to be in-active
        for i in range(1, self.dimension + 1):
            self.cube[z_cord - 1][y_cord - 1][i - 1] = 0

        self.history_remove(x_cord, y_cord, z_cord)
    def history_add(self, x_cord, y_cord, z_cord):
        """adds history in the form (x, y, z)"""
        self.cube_history.append(f'({x_cord},{y_cord},{z_cord})')

    def history_remove(self, x_cord, y_cord, z_cord):
        """removes history in the form (x, y, z)"""
        self.cube_history.remove(f'({x_cord},{y_cord},{z_cord})')

    def history(self):
        history_string = ''
        for cord in self.cube_history:
            history_string += f'{cord} '
        return history_string


    def history_reset(self):
        self.cube_history = []

    def is_solved(self):
        for z_cord in range(1 , self.dimension + 1):
            for y_cord in range(1 , self.dimension + 1):
                for x_cord in range(1, self.dimension + 1):
                    # checks cell in given (x , y , z) cord
                    if self.cube[z_cord - 1][y_cord - 1][x_cord - 1] == 0:
                        return False
        return True

    def is_useless(self,x_cord, y_cord, z_cord):
        useless_bool = True
        if self.cube[z_cord - 1][y_cord - 1][x_cord - 1] == 0:
            useless_bool = False
        # checks if all cords in x , y, x row are inactive
        for cord in range(0, self.dimension):
            if self.cube[z_cord - 1][y_cord - 1][cord] == 0 or self.cube[z_cord - 1][cord][x_cord - 1] == 0 or self.cube[cord][y_cord - 1][x_cord - 1] == 0:
                useless_bool = False
        return useless_bool