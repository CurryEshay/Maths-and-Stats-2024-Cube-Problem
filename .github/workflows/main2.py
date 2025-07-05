from cube_operations import Cube
import tkinter as tk
import ttkbootstrap as ttk
import math
import customtkinter as ctk
from cube_simulation import Simulation
# display layers
class CubeLayer(ctk.CTkFrame):
    # init method
    def __init__(self, colour_active, colour_inactive, parent, layer_list, layer_index):
        super().__init__(master=parent)
        # attributes
        self.colour_active = colour_active
        self.colour_inactive = colour_inactive
        self.layer_list = layer_list
        self.layer_index = layer_index
        self.dimension = len(self.layer_list)
        self.main_frame = ctk.CTkFrame(master = self)
        self.cell_frame = ctk.CTkFrame(master = self.main_frame)
        self.layer_label = ctk.CTkLabel(master = self.main_frame,
                                        text = f'Layer (z cord): {self.layer_index}')
        self.create_layer()
        self.main_frame.pack(expand = True, fill = 'both', padx = 5)
    def create_layer(self):
        # makes n x n grid for cells
        self.layer_label.pack()
        for index in range(1 , self.dimension + 1):
            self.cell_frame.rowconfigure(index = index, weight = 1, uniform = 'a')
            self.cell_frame.columnconfigure(index = index, weight = 1, uniform = 'a')

        for y_index, y_row in enumerate(self.layer_list):
            for x_index, x_cell in enumerate(y_row):
                # if cell is active
                if x_cell >= 1:
                    ctk.CTkLabel(master = self.cell_frame,
                                 bg_color = self.colour_active,
                                 text = f' {x_cell} ').grid(row = y_index + 1, column = x_index + 1, sticky = 'news')
                else:
                    ctk.CTkLabel(master=self.cell_frame,
                                 bg_color=self.colour_inactive,
                                 text=f' {x_cell} ').grid(row=y_index + 1, column= x_index + 1, sticky = 'news')
        self.cell_frame.pack(expand = True, fill = 'both')

    def grid_place(self, grid_row, grid_column):
        self.grid(row = grid_row, column = grid_column, sticky = 'news')

# display for cube
class CubeDisplay(ttk.Canvas):
    """Takes a cube as argument and returns a display for cube"""
    # init method
    def __init__(self, cube):
        super().__init__(master = window)

        # attributes
        self.cube = cube
        self.cube_list = cube.cube
        self.dimension = len(cube)
        self.create_display()

    def create_display(self):
        self.layers = []
        self.layout_frame = ctk.CTkFrame(master=self)
        self.create_grid()
        LAYER_ROW = 1
        LAYER_COLUMN = 1
        for layer_index , layer in enumerate(self.cube_list):
            self.layers.append(CubeLayer(colour_active= 'red',
                                         colour_inactive = 'white',
                                         parent = self.layout_frame,
                                         layer_list = layer,
                                         layer_index = layer_index + 1))
            self.layers[layer_index].grid_place(grid_row = LAYER_ROW, grid_column = LAYER_COLUMN)
            if LAYER_COLUMN == 4:
                LAYER_COLUMN = 0
                LAYER_ROW += 1
            LAYER_COLUMN += 1

        self.layout_frame.pack(expand=True, fill='both')
        self.pack(expand=True, fill='both')

    def create_grid(self):
        self.MAX_COLUMN = 4
        self.NO_ROWS = int(math.ceil(self.dimension / self.MAX_COLUMN))
        # creates requires amount of rows
        for row_index in range(1, self.NO_ROWS + 1):
            self.layout_frame.rowconfigure(index = row_index, weight = 1 ,uniform = 'a')
            # create amount of columns per row
            for column_index in range(1, self.MAX_COLUMN + 1):
                self.layout_frame.columnconfigure(index = column_index, weight = 1, uniform = 'a')
                # ctk.CTkLabel(self.layout_frame, bg_color = 'red').grid(row = row_index, column = column_index, sticky = 'news')

    def remove_grid(self):
        self.layout_frame.pack_forget()
        self.pack_forget()

    def update(self, cube):
        self.remove_grid()
        self.cube = cube
        self.cube_list = cube.cube
        self.dimension = len(cube)
        self.create_display()

    def destroy(self):
        self.pack_forget()

# functions
def set_dimensions(dimensions):
    global display_cube
    global cube
    global history_string_var
    cube = Cube(dimensions)
    print('Cube Created!')
    display_cube.remove_grid()
    display_cube = CubeDisplay(cube = cube)
    cube.history_reset()
    history_string_var.set(f'History 0: Empty')
    spinbox_x_cord.configure(to_ = len(cube))
    spinbox_y_cord.configure(to_ = len(cube))
    spinbox_z_cord.configure(to_ = len(cube))
def set_activate_cell(x_cord, y_cord, z_cord):
    global cube
    global history_string_var
    cube.activate_cell(x_cord,y_cord,z_cord)
    display_cube.update(cube = cube)
    history_string_var.set(f'History {len(cube.history().split(" ")) - 1}: {cube.history()}')

def set_deactivate_cell(x_cord, y_cord, z_cord):
    global cube
    global history_string_var
    cube.deactivate_cell(x_cord, y_cord, z_cord)
    display_cube.update(cube=cube)
    history_string_var.set(f'History {len(cube.history().split(" ")) - 1}: {cube.history()}')

def set_activate_multiple_cells(cords):
    global cube
    global history_string_var
    # final_cords = []
    # separate cords
    cords = cords.split(' ')
    for index, cord in enumerate(cords):
        # formats cord
        cord = cord.replace('(', '')
        cord = cord.replace(')', '')
        # sets old cord as new formatted cord
        cords[index] = cord
        # gets x, y, z for given cord
        cords[index] = cords[index].split(',')

    # activate cells in list
    for cord in cords:
        cube.activate_cell(int(cord[0]), int(cord[1]), int(cord[2]))
        display_cube.update(cube)

    history_string_var.set(f'History {len(cube.history().split(" ")) - 1}: {cube.history()}')





def set_deactivate_multiple_cells(cords):
    global cube
    global history_string_var
    # final_cords = []
    # separate cords
    cords = cords.split(' ')
    for index, cord in enumerate(cords):
        # formats cord
        cord = cord.replace('(', '')
        cord = cord.replace(')', '')
        # sets old cord as new formatted cord
        cords[index] = cord
        # gets x, y, z for given cord
        cords[index] = cords[index].split(',')
    # de activate cells in list
    for cord in cords:
        cube.deactivate_cell(int(cord[0]), int(cord[1]), int(cord[2]))
        display_cube.update(cube)
    history_string_var.set(f'History {len(cube.history().split(" ")) - 1}: {cube.history()}')

# def run_sim(amount, max_solution, dimension):
#     global sim_result_frame
#     solution = ''
#     for i in range(0, amount):
#         sim_cube = Simulation(Cube(dimension = dimension))
#         solution = sim_cube.run_optimal_simulation(UPPER_BOUND = max_solution)
#         ttk.Label(sim_result_frame, text = str(solution)).pack()

# def run_simulation_window():
#     window.quit()
#     sim_window.mainloop()
#     window.mainloop()



# window setup
window = ttk.Window(themename = 'darkly')
ctk.set_appearance_mode("Dark")
window.title('Maths & Stats: Cube Problem')
window.geometry('1000x900')

# default
cube = Cube(4)
# options frame
frame_options = ctk.CTkFrame(window)

# frame for inputting cube dimensions
frame_dimensions = ctk.CTkFrame(frame_options)

# widgets in dimensions frame

# button to update value
btn_update_dimensions = ttk.Button(frame_dimensions,
                                   text = 'set dimensions' ,
                                   command = lambda: set_dimensions(dimensions_int.get()))

# spinbox to input value
dimensions_int = tk.IntVar(value = 4)
spinbox_dimensions = ttk.Spinbox(frame_dimensions,
                                 from_ = 2 ,
                                 to_ = 50,
                                 increment = 1,
                                 textvariable = dimensions_int,
                                 width = 3)

# cube manipulation frame
frame_cube_manipulation = ctk.CTkFrame(frame_options)

# widgets in cube manipulation frame

# buttons to activate or de activate cube
btn_activate = ttk.Button(frame_cube_manipulation, text = 'activate cell',
                          command = lambda: set_activate_cell(x_cord_int.get(), y_cord_int.get(), z_cord_int.get()))
btn_deactivate = ttk.Button(frame_cube_manipulation, text = 'deactivate cell', command = lambda: set_deactivate_cell(x_cord_int.get(), y_cord_int.get(), z_cord_int.get()) )
z_cord_int = tk.IntVar(value = 1)
y_cord_int = tk.IntVar(value = 1)
x_cord_int = tk.IntVar(value = 1)
x_y_z_cord_string = tk.StringVar(value = '(1,1,1) (2,2,2) (3,3,3) (4,4,4)')

# spin boxs to input cords
label_z_cord = ttk.Label(frame_cube_manipulation, text = 'z: ')
label_y_cord = ttk.Label(frame_cube_manipulation, text = 'y: ')
label_x_cord = ttk.Label(frame_cube_manipulation, text = 'x: ')
spinbox_z_cord = ttk.Spinbox(frame_cube_manipulation,
                             from_ = 1,
                             to_ = len(cube),
                             increment = 1,
                             textvariable = z_cord_int,
                             width = 3)
spinbox_y_cord = ttk.Spinbox(frame_cube_manipulation,
                             from_ = 1,
                             to_ = len(cube),
                             increment = 1,
                             textvariable = y_cord_int,
                             width = 3)
spinbox_x_cord = ttk.Spinbox(frame_cube_manipulation,
                             from_ = 1,
                             to_ = len(cube),
                             increment = 1,
                             textvariable = x_cord_int,
                             width = 3)
# activating multiple cells button and entry
btn_activate_multiple_cells = ttk.Button(frame_cube_manipulation,
                                         text = 'activate multiple cells',
                                         command = lambda: set_activate_multiple_cells(x_y_z_cord_string.get()))
btn_deactivate_multiple_cells = ttk.Button(frame_cube_manipulation,
                                         text = 'deactivate multiple cells',
                                         command = lambda: set_deactivate_multiple_cells(x_y_z_cord_string.get()))
label_form_entry = ttk.Label(frame_cube_manipulation, text = 'Form: (x,y,z) (x,y,z) ...')
entry_x_y_z_cord = ttk.Entry(frame_cube_manipulation,
                             textvariable = x_y_z_cord_string)

# button_run_sim_window = ttk.Button(frame_cube_manipulation, text = 'Open Sim', command = run_simulation_window)
# layout cube manipulation frame
btn_activate.pack(side = 'left')
btn_deactivate.pack(side = 'left')
label_x_cord.pack(side = 'left')
spinbox_x_cord.pack(side = 'left')
label_y_cord.pack(side = 'left')
spinbox_y_cord.pack(side = 'left')
label_z_cord.pack(side = 'left')
spinbox_z_cord.pack(side = 'left')
btn_activate_multiple_cells.pack(side = 'left')
btn_deactivate_multiple_cells.pack(side = 'left')
label_form_entry.pack(side = 'left')
entry_x_y_z_cord.pack(side = 'left')
# button_run_sim_window.pack(side = 'left')
frame_cube_manipulation.pack(side = 'left')

# dimensions frame layout
btn_update_dimensions.pack(side = 'left', expand = True, fill = 'x')
spinbox_dimensions.pack(side = 'left', expand = True, fill = 'x')

# packing dimension frame
frame_dimensions.pack()

# packing options frame
frame_options.pack(fill = 'x')

# history frame
history_frame = ctk.CTkFrame(window)
history_string_var = tk.StringVar(value = 'History 0: Empty')
label_history = ttk.Label(history_frame, textvariable = history_string_var)
label_history.pack(side = 'left')
history_frame.pack(fill = 'x')

# default display
display_cube = CubeDisplay(cube)

# simulation window
# sim_window = ttk.Window(themename = 'darkly')
# sim_window.title('Simulation')
# sim_window.geometry('400x300')

# simulation window widgets
# sim_entry_frame = ctk.CTkFrame(sim_window)
# sim_dimensions_int = tk.IntVar()
# sim_max_solution_int = tk.IntVar()
# sim_amount_solution_int = tk.IntVar()
# sim_label_dimensions = ttk.Label(sim_entry_frame, text = 'Enter dimensions of cube')
# sim_label_max_solution = ttk.Label(sim_entry_frame, text = 'Enter maximum solution length')
# sim_label_amount_solution = ttk.Label(sim_entry_frame, text = 'Enter amount of solution')
# sim_spinbox_dimensions = ttk.Spinbox(sim_entry_frame,
#                                  from_ = 2 ,
#                                  to_ = 50,
#                                  increment = 1,
#                                  textvariable = sim_dimensions_int)
# sim_spinbox_max_solution = ttk.Spinbox(sim_entry_frame,
#                                  from_ = 2 ,
#                                  to_ = 1000,
#                                  increment = 1,
#                                  textvariable = sim_max_solution_int)
# sim_spinbox_amount_solution = ttk.Spinbox(sim_entry_frame,
#                                  from_ = 1 ,
#                                  to_ = 1000,
#                                  increment = 1,
#                                  textvariable = sim_amount_solution_int)
# sim_button_run = ttk.Button(sim_entry_frame, text = 'Run simulation',
#                             command = lambda: run_sim(amount = sim_amount_solution_int.get(), max_solution = sim_max_solution_int.get(), dimension = sim_dimensions_int.get()))
#
# sim_result_frame = ctk.CTkScrollableFrame(sim_window)
# # sim window layout
# sim_label_dimensions.pack(side = 'left')
# sim_spinbox_dimensions.pack(side = 'left')
# sim_label_max_solution.pack(side = 'left')
# sim_spinbox_max_solution.pack(side = 'left')
# sim_label_amount_solution.pack(side = 'left')
# sim_spinbox_amount_solution.pack(side = 'left')
# sim_button_run.pack(side = 'left')
# sim_entry_frame.pack()
# run
window.mainloop()
