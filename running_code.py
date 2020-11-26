from datetime import datetime

from Simulation import Simulation
'''
There are different adjustments you can make to the Simulation.

room:
There are different rooms to choose from:
    -"square": a standart square room with one exit
    -"long_room": a standart rectangle room with one exit
    -"long_room_v2": a rectangle room with two exits. Half of the agents will go to each exit
    -"edu_11", "edu_1", "edu_room": square rooms with one exit and different walls inside the room

You can choose the number of agents in the simulation with "num_individuals".

"num_steps" is the duraten the simulation will runn (recommended:1000)

"method" is the method of integration. You should use leap_frog even though it will often explode
since more relaible methods of integration like ode45 and monto carlo take a lot a computational power.
'''
# calls the simulation with 3 agents, 1000 timesteps, and the leap_frog methode 
# for integration and the standart square room

def take_time(string_time):
    now = datetime.now()
    time = now.strftime("%H:%M:%S")
    print(string_time, " time:", time)


def simulating_proccess(num_of_idividuals, center=False):
    take_time("Start " + str(count_individuals))
    sim = Simulation(num_individuals=num_of_idividuals, num_steps=9000, center=center)
    sim.fill_room()  # fills the spawn zone with random people
    sim.run()  # runs the simulation
    take_time("End " + str(count_individuals))
    sim.show(wait_time=50, sim_size=600)   # displays the solutions to the simulations in pygame with


if __name__ == '__main__':

    is_center = False
    for count_individuals in [1]:
        simulating_proccess(count_individuals, is_center)
