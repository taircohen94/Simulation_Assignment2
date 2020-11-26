import numpy as np

class Room:

    def __init__(self, width, height, num_of_doors=1, center=False):
        self.room_height = height
        self.room_width = width
        self.room_size = self.room_height * self.room_width


if __name__ == '__main__':
    room_size = 10
    spawn_zone = np.array([[room_size / 2, room_size - 1], [1, room_size - 1]])
    print(spawn_zone)







