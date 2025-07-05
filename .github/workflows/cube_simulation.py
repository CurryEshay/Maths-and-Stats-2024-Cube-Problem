from cube_operations import Cube
import math
import random
class Simulation:
    """runs a simulation for a given cube"""
    # attributes
    def __init__(self, cube):
        self.cube = cube
        self.cube.reset_cube()
        self.dimension = len(cube)
        self.cache_cube = Cube(self.dimension)
        self.create_sample_space()
    def create_sample_space(self):
        self.sample_space = []
        for z_cord in range(1 , self.dimension + 1):
            self.sample_space.append([])
            for y_cord in range(1 , self.dimension + 1):
                for x_cord in range(1, self.dimension + 1):
                    self.sample_space[z_cord - 1].append((x_cord, y_cord, z_cord))
    def run_optimal_simulation(self, UPPER_BOUND):
        while True:
            self.cube.reset_cube()
            self.create_sample_space()
            COUNT = 0
            print(self.cube.history())
            # choose random cubes in each layer
            while True:
                for index,layer in enumerate(self.sample_space):
                    random_choice = random.choice(layer)
                    # activate random choice
                    self.cube.activate_cell(random_choice[0], random_choice[1], random_choice[2])
                    # removes chosen option
                    self.sample_space[index].remove(random_choice)
                    COUNT += 1
                    # checks if any cords are useless
                    for check_index, check_layer in enumerate(self.sample_space):
                        for check_cord in check_layer:
                            if self.cube.is_useless(check_cord[0], check_cord[1], check_cord[2]):
                                self.sample_space[check_index].remove(check_cord)

                    if self.cube.is_solved():
                        history = self.cube.history()
                        self.cube.reset_cube()
                        return history

                    if COUNT >= UPPER_BOUND:
                        self.cube.reset_cube()
                        self.create_sample_space()
                        COUNT = 0


sim = Simulation(Cube(4))
print(sim.run_optimal_simulation(15))