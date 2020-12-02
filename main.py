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
    # num_of_steps_list = []
    # all_positions_list = []
    # for i in range(200):
    #     sim = Simulation(door_position=door_pos, room_width=room_width,
    #                      room_height=room_height, center=False)
    #     take_time("Start")
    #     num_of_steps, all_pos, all_v = sim.run()
    #     num_of_steps_list.append(num_of_steps)
    #     all_positions_list.append(all_pos)
    #     take_time("End " + str(num_of_steps) + " Steps")
    #
    # max_steps = max(num_of_steps_list)
    # print("The max time to escape from the room is: " + str(max_steps))
    # # find the best fit distribution of the num of steps that takes to the entities to escape from a room
    # # f = Fitter(num_of_steps_list)
    # # f.fit()
    # # f.summary()
    # # f.plot_pdf()
    # run_distribution(num_of_steps_list)

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
    # print("#############################  Q2.A   #########################")
    # num_of_steps_list_Q2A = []
    # all_positions_list_Q2A = []
    # for i in [20, 50, 100, 200]:
    #     sim = Simulation(num_individuals=i, door_position=door_pos, room_width=room_width,
    #                      room_height=room_height, center=False)
    #     take_time("Start Simulation with " + str(i) + " entities")
    #
    #     num_of_steps, all_pos, all_v, escaped = sim.run()
    #     num_of_steps_list_Q2A.append(num_of_steps)
    #     all_positions_list_Q2A.append(all_pos)
    #     take_time("End Simulation with " + str(i) + " entities , num of steps: "+str(num_of_steps) + " , Escaped: "+str(len(escaped)))

    # ------------ end Q2.A ------------

    # ------------ Q2.B ------------
    print("#############################  Q2.B   #########################")
    num_of_steps_list_Q2A = []
    all_positions_list_Q2A = []
    num_of_ppl = 20
    v0 = 0.1
    dict_v_k = {}
    for i in range(0, 100):
        print(i)
        v = v0 + i * 0.1
        sim = Simulation(num_individuals=50, door_position=door_pos, room_width=room_width,
                         room_height=room_height, center=False, v0=v)
        # take_time("Start Simulation with " + str(i) + " entities")

        num_of_steps, all_pos, all_v, escaped = sim.run()
        dict_v_k[v] = num_of_steps
        # take_time("End Simulation with " + str(i) + " entities , num of steps: " + str(num_of_steps))

    lists = sorted(dict_v_k.items())  # sorted by key, return a list of tuples

    x, y = zip(*lists)  # unpack a list of pairs into two tuples

    plt.plot(x, y)
    plt.show()

    # ------------ end Q2.B ------------

    # # ------------ Q2.C ------------
    # print("#############################  Q2.C   #########################")
    #
    # num_of_steps_list_Q2A = []
    # all_positions_list_Q2A = []
    #
    # for i in [50] * 100:
    #     sim = Simulation(num_individuals=i, door_position=door_pos, room_width=room_width,
    #                      room_height=room_height, center=False, oldppl=True)
    #     # take_time("Start Simulation with " + str(i) + " entities")
    #
    #     num_of_steps, all_pos, all_v, escaped = sim.run()
    #     num_of_steps_list_Q2A.append(num_of_steps)
    #     all_positions_list_Q2A.append(all_pos)
    #     # take_time("End Simulation with " + str(i) + " entities , num of steps: " + str(num_of_steps))
    #
    # print((sum(num_of_steps_list_Q2A) )/ len(num_of_steps_list_Q2A) )
    # nine_list = [x for x in num_of_steps_list_Q2A if x == 9000]
    # print((sum(num_of_steps_list_Q2A) - sum(nine_list) )/ (len(num_of_steps_list_Q2A) - len(nine_list)))
    # print(len(nine_list))
    #
    #     # ------------ end Q2.C ------------

    # ------------ Q3.A ------------
    # num_of_steps_list_Q2A = []
    # all_positions_list_Q2A = []
    # door2_pos = Position(0, room_height / 2)
    #
    # for i in [20, 50, 100, 200]:
    #     sim = Simulation(num_individuals=i, door_position=door_pos, room_width=room_width,
    #                      room_height=room_height, center=False, oldppl=False, door2_pos=door2_pos)
    #     take_time("Start Simulation with " + str(i) + " entities")
    #
    #     num_of_steps, all_pos, all_v, escaped = sim.run()
    #
    #     take_time("End Simulation with " + str(i) + " entities , num of steps: " + str(num_of_steps) + " , Escaped: " + str(len(escaped)))

    # ------------ end Q3.A ------------

    # ------------ Q3.B ------------
    # num_of_steps_list_Q2A = []
    # all_positions_list_Q2A = []
    # door2_pos = Position(0, room_height / 2)
    #
    # for i in [20] * 10:
    #     sim = Simulation(num_individuals=i, door_position=door_pos, room_width=room_width,
    #                      room_height=room_height, center=False, oldppl=False, door2_pos=door2_pos, entity_know_both_door=False)
    #     take_time("Start Simulation with " + str(i) + " entities")
    #
    #     num_of_steps, all_pos, all_v, escaped = sim.run()
    #
    #     take_time("End Simulation with " + str(i) + " entities , num of steps: " + str(num_of_steps) + " , Escaped: " + str(len(escaped)))

    # ------------ end Q3.B ------------

    # ------------ Q3.C ------------
    # num_of_steps_list_Q2A = []
    # all_positions_list_Q2A = []
    # door2_pos = Position(0, room_height / 2)
    #
    # for i in [20] * 10:
    #     sim = Simulation(num_individuals=i, door_position=door_pos, room_width=room_width,
    #                      room_height=room_height, center=False, oldppl=False             )
    #     take_time("Start Simulation with " + str(i) + " entities")
    #
    #     num_of_steps, all_pos, all_v, escaped = sim.run3c()
    #
    #     take_time("End Simulation with " + str(i) + " entities , num of steps: " + str(num_of_steps) + " , Escaped: " + str(len(escaped)))

    # ------------ end Q3.C ------------

    # ------------ Q4.C ------------
    # print("#############################  Q4   #########################")
    # num_of_steps_list_Q2A = []
    # all_positions_list_Q2A = []
    # door2_pos = Position(0, room_height / 2)
    #
    # for i in [20, 50, 100, 200]:
    #     sim = Simulation(num_individuals=i, door_position=door_pos, room_width=room_width,
    #                      room_height=room_height, center=False, door2_pos=door2_pos)
    #     take_time("Start Simulation with " + str(i) + " entities")
    #
    #     num_of_steps, all_pos, all_v, escaped = sim.run()
    #     num_of_steps_list_Q2A.append(num_of_steps)
    #     all_positions_list_Q2A.append(all_pos)
    #     take_time("End Simulation with " + str(i) + " entities , num of steps: "+str(num_of_steps) + " , Escaped: "+str(len(escaped)))

    # ------------ end Q4 ------------
