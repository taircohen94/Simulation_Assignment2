import numpy as np

class Room:

    def __init__(self, width, height, num_of_doors=1, center=False):
        self.room_height = height
        self.room_width = width
        self.room_size = self.room_height * self.room_width
        self.wallshere = False
        self.door_size = 10
        if num_of_doors == 1:
            self.destination = np.array([[self.room_size + 10, self.room_size / 2]])  # destination the agenst want to go
            self.num_walls = 5
            self.walls = np.array([[[0, 0], [0, self.room_size]],  # Y1
                                   [[0, self.room_size], [self.room_size, self.room_size]],  #2
                                   [[self.room_size, self.room_size / 2 + self.door_size / 2], [self.room_size, self.room_size]],  # wall 3
                                   [[self.room_size, self.room_size / 2 - self.door_size / 2], [self.room_size, 0]],  # wall 4
                                   [[self.room_size, 0], [0, 0]]])  # wall 5
            # agents spawn with x and y position between 1 and (room_size-1)
            if not center:
                self.spawn_zone = np.array([[1, self.room_size - 1], [1, self.room_size - 1]])
            else:
                self.spawn_zone = np.array([[self.room_height/2 -0.5, self.room_width/2-0.5], [self.room_height/2-0.5, self.room_width/2+0.5]])

        if num_of_doors == 2:
            self.destination = np.array([[room_size + 0.5, room_size / 2]])  # destination the agenst want to go
            self.num_walls = 6
            self.walls = np.array([[[0, 0], [0, room_size]],  # Y
                                   [[0, room_size], [room_size, room_size]],  #
                                   [[room_size, room_size], [room_size, room_size / 2 + self.door_size / 2]],  # wall 4
                                   [[room_size, room_size / 2 - self.door_size / 2], [room_size, 0]],  # wall 4
                                   [[room_size, 0], [0, 0]]])  # wall 5
            # agents spawn with x and y position between 1 and (room_size-1)
            self.spawn_zone = np.array([[1, self.room_height - 1], [1, self.room_width - 1]])

    def get_wall(self, n):  # gives back the endpoints of the nth wall
        return self.walls[n, :, :]

    def get_num_walls(self):  # gives back the number of walls
        return self.num_walls

    def get_spawn_zone(self):  # gives back the spawn_zone
        return self.spawn_zone

    def get_room_size(self):  # gives back the size of the room
        return self.room_size

    def get_destination(self):  # gives back the destination the agents want to get to
        return self.destination



if __name__ == '__main__':
    room_size = 10
    spawn_zone = np.array([[room_size / 2, room_size - 1], [1, room_size - 1]])
    print(spawn_zone)







