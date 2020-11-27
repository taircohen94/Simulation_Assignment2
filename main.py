from datetime import datetime
from typing import List, Any

from matplotlib import pyplot as plt
from Position import Position
from Simulation import Simulation
# from fitter import Fitter
from BestFitDistribution import *

def collapse(x1, x2, y1, y2):
    return pow(pow(abs(x1 - x2), 2) + pow(abs(y1 - y2), 2), 0.5) < 0.5


def take_time(string_time):
    now = datetime.now()
    time = now.strftime("%H:%M:%S")
    print(string_time, "time:", time)


if __name__ == '__main__':
    # ------------ Q1.A ------------
    room_width = 15
    room_height = 15
    door_pos = Position(room_width, room_height / 2)
    # sim = Simulation(door_position=door_pos, room_width=room_width, room_height=room_height, center=True)
    # take_time("Start")
    # num_of_steps, all_pos, all_v = sim.run()
    # all_vx = [v.x for v in all_v]
    # all_vy = [v.y for v in all_v]
    #
    # plt.plot(range(0, num_of_steps), all_vx)
    # plt.xlabel('Time Step')
    # plt.ylabel('X Velocity')
    #
    # plt.title('X Velocity / Time Step ')
    # plt.show()
    # plt.plot(range(0, num_of_steps), all_vy, color='r')
    # plt.xlabel('Time Step')
    # plt.ylabel('Y Velocity')
    #
    # plt.title('Y Velocity / Time Step ')
    # plt.show()
    #
    # all_pos_x = [p.x for p in all_pos]
    # all_pos_y = [p.y for p in all_pos]
    # plt.plot(range(0, num_of_steps), all_pos_x, color='g')
    # plt.xlabel('Time Step')
    # plt.ylabel('X axis Position')
    #
    # plt.title('X axis Position / Time Step ')
    # plt.show()
    #
    # plt.plot(range(0, num_of_steps), all_pos_y, color='g')
    # plt.xlabel('Time Step')
    # plt.ylabel('Y axis Position')
    #
    # plt.title('Y axis Position / Time Step ')
    # plt.show()
    #
    # take_time("End " + str(num_of_steps) + " Steps")
    # ------------ end Q1.A ------------

    # ------------ Q1.B ------------
    num_of_steps_list = []
    all_positions_list = []
    for i in range(200):
        sim = Simulation(door_position=door_pos, room_width=room_width,
                         room_height=room_height, center=False)
        take_time("Start")
        num_of_steps, all_pos, all_v = sim.run()
        num_of_steps_list.append(num_of_steps)
        all_positions_list.append(all_pos)
        take_time("End " + str(num_of_steps) + " Steps")

    max_steps = max(num_of_steps_list)
    print("The max time to escape from the room is: " + str(max_steps))
    # find the best fit distribution of the num of steps that takes to the entities to escape from a room
    # f = Fitter(num_of_steps_list)
    # f.fit()
    # f.summary()
    # f.plot_pdf()
    run_distribution(num_of_steps_list)

    # ------------ end Q1.B ------------

    # ------------ end Q1.C ------------

    # collapse_counter = 0
    # for j in range(0, 199):
    #     for k in range(j + 1, 200):
    #         min_length = min(len(all_positions_list[j]), len(all_positions_list[k]))
    #         for index in range(0, min_length):
    #             if collapse(all_positions_list[j][index].x,
    #                         all_positions_list[k][index].x,
    #                         all_positions_list[j][index].y,
    #                         all_positions_list[k][index].y):
    #                 collapse_counter += 1
    #
    # print(collapse_counter)

    # ------------ end Q1.C ------------

    # ------------ Q2.A ------------
    # num_of_steps_list_Q2A = []
    # all_positions_list_Q2A = []
    # for i in [20, 50, 100, 200]:
    #     # door position like 1A - (room_width, room_height / 2)
    #     sim = Simulation(num_individuals=i, door_position=door_pos, room_width=room_width,
    #                      room_height=room_height, center=False)
    #     take_time("Start Simulation with " + str(i) + " entities")
    #
    #     num_of_steps, all_pos, all_v = sim.run()
    #     num_of_steps_list_Q2A.append(num_of_steps)
    #     all_positions_list_Q2A.append(all_pos)
    #     take_time("End Simulation with " + str(i) + " entities ")
    #     print(all_positions_list_Q2A)

    # ------------ end Q2.A ------------

    # ------------ Q2.B ------------
    # ------------ end Q2.B ------------

    # ------------ Q2.C ------------
    # ------------ end Q2.C ------------

    # ------------ Q3.A ------------
    # ------------ end Q3.A ------------

    # ------------ Q3.B ------------
    # ------------ end Q3.B ------------

    # ------------ Q3.C ------------
    # ------------ end Q3.C ------------
