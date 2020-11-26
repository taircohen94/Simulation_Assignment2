import numpy as np
import sys

from diff_equation import Diff_Equ

import pygame
from steps_function_quit import display_events
from steps_function_quit import display_graph

from Room import Room

import Integrators
from Integrators import leap_frog

'''
class to put the hole thing together. Its main parts
are the Differential Equation, the rooms, and the method 
of integration. The Integration can be done by calling
the run function. If the integration is done the results 
are saved in self.y for later use for example to display
them with with the function "Show"'''


class Simulation:
    def __init__(self, num_individuals=2, num_steps=9000,
                 tau=0.01, v_des=1.5, num_of_doors=1,
                 room_width=15, room_height=15):

        std_deviation = 0.07
        variation = np.random.normal(loc=1, scale=std_deviation,
                                     size=(1, num_individuals))  # is late used to make the agents differ in weight and size

        # Constants
        self.L = room_width * room_height  # size of square room (m)
        self.N = num_individuals  # quantity of pedestrians
        self.tau = tau  # time-step (s)
        self.num_steps = num_steps  # number of steps for integration

        # Agent information
        self.radii = 0.4 * (np.ones(self.N) * variation).squeeze()  # radii of pedestrians (m)
        self.v_des = v_des * np.ones(self.N)  # desired velocity (m/s)
        self.m = 80 * (np.ones(self.N) * variation).squeeze()  # mass of pedestrians (kg)
        self.forces = None  # forces on the agents
        self.agents_escaped = None  # number of agents escaped by timesteps
        self.v = np.zeros((2, self.N, self.num_steps))  # Three dimensional array of velocity
        self.r = np.zeros(
            (2, self.N, self.num_steps))  # Three dimensional array of place: x = coordinates, y = Agent, z=Time

        # other
        self.room = Room(room_width, room_height, num_of_doors)  # kind of room the simulation runs in
        # self.method =   # method used for integration
        self.diff_equ = Diff_Equ(self.N, self.L, self.tau, self.room, self.radii,
                                 self.m)  # initialize Differential equation

    # function set_time, set_steps give the possiblity to late change these variable when needed
    def set_steps(self, steps):
        self.num_steps = steps

    # function to change the methode of integration if needed
    def set_methode(self, method):
        self.method = getattr(Integrators, method)

    def dont_touch(self, i, x):  # yields false if people don't touch each other and true if they do
        for j in range(i - 1):
            if np.linalg.norm(x - self.r[:, j, 0]) < 3 * self.radii[i]:
                return True
        return False

    # fills the spawn zone with agents with random positions
    def fill_room(self):
        spawn = self.room.get_spawn_zone()
        len_right = spawn[0, 1] - spawn[0, 0]
        len_left = spawn[1, 1] - spawn[1, 0]
        max_len = max(len_left, len_right)

        # checks if the area is too small for the agents to fit in
        area_people = 0
        for i in range(self.N):
            area_people += 4 * self.radii[i] ** 2
        if area_people >= 0.7 * max_len ** 2:
            sys.exit('Too much people! Please change the size of the room/spawn-zone or the amount of people.')
        # checks if the agent touches another agent/wall and if so gives it a new random position in the spawn-zone 
        for i in range(self.N):
            # The pedestrians don't touch the wall
            x = len_right * np.random.rand() + spawn[0, 0]
            y = len_left * np.random.rand() + spawn[1, 0]
            pos = [x, y]

            # The pedestrians don't touch each other
            while self.dont_touch(i, x):
                x = len_right * np.random.rand() + spawn[0, 0]
                y = len_left * np.random.rand() + spawn[1, 0]
                pos = [x, y]
            self.r[:, i, 0] = pos

        self.v[:, :, 0] = self.v_des * self.diff_equ.e_t(self.r[:, :, 0])

    # calls the method of integration with the starting positions, diffequatial equation, number of steps, and delta t = tau
    def run(self):
        self.r, self.agents_escaped, self.forces = self.method(self.r[:, :, 0], self.v[:, :, 0], self.diff_equ.f,
                                                               self.num_steps, self.tau, self.room)

    # Displayes the simulation in pygame
    def show(self, wait_time, sim_size):
        display_graph(self.agents_escaped, self.forces, self.m)
        display_events(self.r, self.room, wait_time, self.radii, sim_size, self.agents_escaped)