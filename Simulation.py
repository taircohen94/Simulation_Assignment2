
MAX_INDIVIDUALS = 250

class Simulation:

    def __init__(self, num_individuals=1, num_steps=9000,
                 tau=0.01, v_des=1.5, num_of_doors=1,
                 room_width=15, room_height=15, center=False):
        self.num_individuals = num_individuals