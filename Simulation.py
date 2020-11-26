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
MAX_INDIVIDUALS = 250

class Simulation:

    def __init__(self, num_individuals=1, num_steps=9000,
                 tau=0.01, v_des=1.5, num_of_doors=1,
                 room_width=15, room_height=15, center=False):
        num_individuals = num_individuals if num_individuals < MAX_INDIVIDUALS else MAX_INDIVIDUALS
        std_deviation = 0.07
        variation = np.random.normal(loc=1, scale=std_deviation, size=(
        1, num_individuals))  # is late used to make the agents differ in weight and size

        # Constants
        self.L = room_width * room_height  # size of square room (m)
        self.N = num_individuals  # quantity of pedestrians
        self.tau = tau  # time-step (s)
        self.num_steps = num_steps  # number of steps for integration

        # Agent information
        self.radii = [0.4 * (np.ones(self.N) * variation).squeeze()] if self.N == 1 else 0.4 * (np.ones(self.N) * variation).squeeze()  # radii of pedestrians (m)
        self.v_des = v_des * np.ones(self.N)  # desired velocity (m/s)
        self.m = 80 * (np.ones(self.N) * variation).squeeze() if self.N > 1 else [80 * (np.ones(self.N) * variation).squeeze()]  # mass of pedestrians (kg)
        self.forces = None  # forces on the agents
        self.agents_escaped = None  # number of agents escaped by timesteps
        self.v = np.zeros((2, self.N, self.num_steps))  # Three dimensional array of velocity
        self.r = np.zeros(
            (2, self.N, self.num_steps))  # Three dimensional array of place: x = coordinates, y = Agent, z=Time

        # other
        self.room = Room(room_width, room_height, num_of_doors, center=center)  # kind of room the simulation runs in
        self.method = self.leap_frog  # method used for integration
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
        self.r, self.agents_escaped, self.forces = self.method(self.r[:, :, 0], self.v[:, :, 0],
                                                               self.diff_equ.f,
                                                               self.num_steps, self.tau, self.room)

    # Displayes the simulation in pygame
    def show(self, wait_time, sim_size):
        display_graph(self.agents_escaped, self.forces, self.m)
        display_events(self.r, self.room, wait_time, self.radii, sim_size, self.agents_escaped)

    def leap_frog(self, y0, v0, f, N_steps, dt, room):

        tmp = 0
        agents_escaped = np.zeros(N_steps)

        y = np.zeros((y0.shape[0], y0.shape[1], N_steps))
        v = np.zeros((y0.shape[0], y0.shape[1], N_steps))
        a = np.zeros((y0.shape[0], y0.shape[1], N_steps))

        y[:, :, 0] = y0
        v[:, :, 0] += 0.5 * dt * f(y[:, :, 0], v[:, :, 0])
        # v[:,:,0] = v0 + 0.5*dt*f(y0)

        for k in range(N_steps - 1):
            # print(100*k/N_steps, '% done.')
            y[:, :, k + 1] = y[:, :, k] + dt * v[:, :, k]
            a[:, :, k] = f(y[:, :, k], v[:, :, k])
            v[:, :, k + 1] = v[:, :, k] + dt * f(y[:, :, k + 1], v[:, :, k] + dt * a[:, :, k])

            for i in range(y.shape[1]):
                # checks if there are two destination and calculates the distance to the closets destination
                destination = np.zeros(len(room.get_destination()))
                for count, des in enumerate(room.get_destination()):
                    destination[count] = np.linalg.norm(y[:, i, k + 1] - des)
                distance = np.amin(destination)

                if distance < 0.1:
                    # we have to use position of door here instead of (0,5)
                    y[:, i, k + 1] = 10 ** 6 * np.random.rand(2)
                    # as well we have to change the  to some c*radii
                    tmp += 1

            agents_escaped[k + 1] = tmp

        return y, agents_escaped, a