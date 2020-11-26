from datetime import datetime
from matplotlib import pyplot as plt
from Position import Position
from Simulation import Simulation


def take_time(string_time):
    now = datetime.now()
    time = now.strftime("%H:%M:%S")
    print(string_time, "time:", time)


if __name__ == '__main__':
    room_width = 15
    room_height = 15
    door_pos = Position(room_width, room_height/2)
    sim = Simulation(door_position=door_pos, room_width=room_width, room_height=room_height, center=True)
    take_time("Start")
    num_of_steps, all_pos, all_v = sim.run()
    all_vx = [v.x for v in all_v]
    all_vy = [v.y for v in all_v]

    plt.plot(range(0, num_of_steps), all_vx)
    plt.xlabel('Time Step')
    plt.ylabel('X Velocity')

    plt.title('X Velocity / Time Step ')
    plt.show()
    plt.plot(range(0, num_of_steps), all_vy, color='r')
    plt.xlabel('Time Step')
    plt.ylabel('Y Velocity')

    plt.title('Y Velocity / Time Step ')
    plt.show()

    all_pos_x = [p.x for p in all_pos]
    all_pos_y = [p.y for p in all_pos]
    plt.plot(range(0, num_of_steps), all_pos_x, color='g')
    plt.xlabel('Time Step')
    plt.ylabel('X axis Position')

    plt.title('X axis Position / Time Step ')
    plt.show()

    plt.plot(range(0, num_of_steps), all_pos_y, color='g')
    plt.xlabel('Time Step')
    plt.ylabel('Y axis Position')

    plt.title('Y axis Position / Time Step ')
    plt.show()



    take_time("End " + str(num_of_steps) + " Steps")
