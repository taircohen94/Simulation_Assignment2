import uuid

from Position import Position


class Entity:

    def __init__(self, initial_position, v0=1.5):
        self.position = initial_position
        self.v0 = v0
        self.acc_time = 0.5
        self.velocity = Position(0, 0)
        self.tau = 0.01
        self.tracked_positions = []
        self.escaped_time = 0
        self.id = uuid.uuid4()

    def dvi_dt(self, ei0):
        new_v = Position(0, 0)
        new_v.x = ((self.v0 * ei0.x - self.velocity.x)*self.tau/self.acc_time) # multiplying by tau for the time correction
        new_v.y = ((self.v0 * ei0.y - self.velocity.y)*self.tau/self.acc_time)
        return new_v

    def ei_dir(self, destination):
        e = Position(0, 0)
        e.x = destination.x - self.position.x
        e.y = destination.y - self.position.y

        dist = self.position.get_dist(destination)
        e.x = e.x/dist
        e.y = e.y/dist

        return e

    def reached_dest(self, dest):
        return self.position.get_dist(dest) <= 0.5

    # def reached_dest(self, door_location):
    #     if door_location.x == 15 or door_location.x == 0:
    #         if self.position.x >= door_location.x and abs(self.position.y-door_location.y) <= 0.5:
    #             return True
    #     return False

    def track_position(self):
        self.tracked_positions.append(self.position)

    def __eq__(self, other):
        if isinstance(other, Entity):
            return other.id == self.id
