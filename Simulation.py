import copy
from random import randint

from Entity import Entity
from Position import Position

MAX_INDIVIDUALS = 250


class Simulation:

    def __init__(self, door_position, num_individuals=1, num_steps=9000, num_of_doors=1, room_width=15, room_height=15,
                 center=False, oldppl=False, v0=1.5, door2_pos = None):
        self.num_individuals = num_individuals
        self.room_height = room_height
        self.room_width = room_width
        self.door_position = door_position
        self.door2_pos = door2_pos
        self.oldppl = oldppl
        self.entities = self.generate_entities(num_individuals,v0, center)
        self.max_step = num_steps
        self.escaped = []


    def generate_entities(self, num_of_entities,v0, center=False):
        entities = []
        inserted_pos = set()
        for index in range(num_of_entities):
            if not center:
                not_exist = False
                pos = None
                while not not_exist:
                    not_exist = False
                    x = randint(0, self.room_width)
                    y = randint(0, self.room_height)
                    if not (x, y) in inserted_pos:
                        pos = Position(x, y)
                        inserted_pos.add((x, y))
                        not_exist = True
            else:
                pos = Position(self.room_width / 2, self.room_height / 2)

            if self.oldppl:
                if index <= num_of_entities * 0.2:
                    entities.append(Entity(pos, v0=0.5))
                else:
                    entities.append(Entity(pos))
            else:
                entities.append(Entity(pos, v0))

        sorted(entities, key=lambda entity: entity.position.get_dist(self.door_position))
        return entities

    def run(self):
        k = 0
        all_velocities = []
        temp_entities = copy.deepcopy(self.entities)

        while k < self.max_step and not len(temp_entities) == 0:
            for entity in temp_entities:
                all_velocities.append(entity.velocity)
                # if there is no one close to me calculate new v,pos etc....
                door_to_test = self.door_position
                if self.door2_pos:
                    # Check which door is closer
                    dist_to_door_1 = entity.position.get_dist(self.door_position)
                    dist_to_door_2 = entity.position.get_dist(self.door2_pos)
                    door_to_test = self.door_position if dist_to_door_1 <= dist_to_door_2 else self.door2_pos

                if not self.is_someone_closer(entity, door_to_test):

                    # Should return ei0 as a position

                    ei0 = entity.ei_dir(door_to_test)

                    # should return velocity as a position
                    new_velocity = entity.dvi_dt(ei0)

                    # add the calculated velocity to the entity
                    entity.velocity += new_velocity

                    temp_location = Position(entity.position.x + entity.velocity.x * entity.tau,
                                             entity.position.y + entity.velocity.y * entity.tau)

                    entity.position = copy.deepcopy(temp_location)
                    entity.track_position()

                    if entity.reached_dest(door_to_test):
                        temp_entities.remove(entity)
                        self.escaped.append(entity)
                        entity.escaped_time = k
                        break
                else:
                    pass
                    # print("no one closer")

            # Increment Time Step
            k += 1
        return k, self.get_all_entities_positions(), all_velocities

    def is_someone_closer(self, specified_entity, door_to_reach):
        # print("test door", door_to_reach)
        specified_entity_dist_to_door = specified_entity.position.get_dist(door_to_reach)
        for e in self.entities:
            if e != specified_entity:
                other_dist_to_door = e.position.get_dist(door_to_reach)
                if specified_entity.reached_dest(e.position) and (specified_entity_dist_to_door >= other_dist_to_door):
                    return True

        return False

    def get_all_entities_positions(self):
        all_positions = []
        for entity in self.escaped:
            for position in entity.tracked_positions:
                all_positions.append(position)

        return all_positions
