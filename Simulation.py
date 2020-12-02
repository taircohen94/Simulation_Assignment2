import copy
from random import randint,uniform

import numpy

from Entity import Entity
from Position import Position

MAX_INDIVIDUALS = 250


class Simulation:

    def __init__(self, door_position, num_individuals=1, num_steps=9000, room_width=15, room_height=15,
                 center=False, oldppl=False, v0=1.5, door2_pos=None, entity_know_both_door=True):
        self.num_individuals = num_individuals
        self.room_height = room_height
        self.room_width = room_width
        self.door_position = door_position
        self.door2_pos = door2_pos
        self.oldppl = oldppl
        self.ekbd = entity_know_both_door
        self.entities = self.generate_entities(num_individuals,v0, center)
        self.max_step = num_steps
        self.escaped = []


    def generate_entities(self, num_of_entities,v0, center=False):
        entities = []
        inserted_pos = set()
        for index in range(num_of_entities):

            # For Q3.b shoud half of the entities know only 1 door
            if not self.ekbd and self.door2_pos:
                num_of_doors = 1 if uniform(1, 2) - 1.5 < 0 else 2
            elif self.door2_pos:
                num_of_doors = 2
            else:
                num_of_doors = 1

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
                entities.append(Entity(pos, v0, num_of_doors=num_of_doors))

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
                if self.door2_pos and entity.num_of_doors == 2:
                    # Check which door is closer
                    dist_to_door_1 = entity.position.get_dist(self.door_position)
                    dist_to_door_2 = entity.position.get_dist(self.door2_pos)
                    if dist_to_door_1 <= dist_to_door_2:
                        door_to_test = self.door_position
                    else:
                        door_to_test = self.door2_pos

                if not self.is_someone_closer(entity, door_to_test, temp_entities):

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

                    if entity.reached_dest(door_to_test, max_radius=7.5):
                        temp_entities.remove(entity)
                        self.escaped.append(entity)
                        entity.escaped_time = k
                        # break
                else:
                    pass
                    # print("no one closer")

            # Increment Time Step
            k += 1
        return k, self.get_all_entities_positions(), all_velocities, self.escaped


    def run3c(self):
        k = 0
        all_velocities = []
        temp_entities = copy.deepcopy(self.entities)

        while k < self.max_step and not len(temp_entities) == 0:
            for entity in temp_entities:
                all_velocities.append(entity.velocity)

                # if entity is close to door in 5m then run to door
                # if there is no one close to me calculate new v,pos etc....
                dist_to_door_1 = entity.position.get_dist(self.door_position)
                dist_to_door_2 = None
                if self.door2_pos:
                    # Check which door is closer
                    dist_to_door_2 = entity.position.get_dist(self.door2_pos)

                if dist_to_door_1 <= 5:
                    door_to_test = self.door_position
                elif dist_to_door_2 and dist_to_door_2 <= 5:
                    door_to_test = self.door2_pos
                else:
                    door_to_test = None

                if door_to_test:
                    if not self.is_someone_closer(entity, door_to_test, temp_entities):

                        # Should return ei0 as a position

                        ei0 = entity.ei_dir(door_to_test)
                        entity.ei = ei0
                        self.set_entity_position(entity, ei0)

                        if entity.reached_dest(door_to_test):
                            temp_entities.remove(entity)
                            self.escaped.append(entity)
                            entity.escaped_time = k
                            # break

                # else run with other ppl in 5m from you
                else:
                    all_5m_ppl = self.get_all_entities_in_5m(entity)
                    ei_avg = self.pos_avg(all_5m_ppl)
                    self.set_entity_position(entity, ei_avg)

            # Increment Time Step
            k += 1
        return k, self.get_all_entities_positions(), all_velocities, self.escaped

    def set_entity_position(self, entity, ei0):
        # should return velocity as a position
        new_velocity = entity.dvi_dt(ei0)
        # add the calculated velocity to the entity
        entity.velocity += new_velocity
        temp_location = Position(entity.position.x + entity.velocity.x * entity.tau,
                                 entity.position.y + entity.velocity.y * entity.tau)
        entity.position = copy.deepcopy(temp_location)
        entity.track_position()

    def is_someone_closer(self, specified_entity, door_to_reach, entities_to_check):
        """
        if specified_entity is the closest one to the door and there is no other entity
        in radius of 0.5 from it then return False (There is no one else closer) and i can move forward
        :param specified_entity:
        :param door_to_reach:
        :param entities_to_check:
        :return:
        """
        # print("test door", door_to_reach)
        specified_entity_dist_to_door = specified_entity.position.get_dist(door_to_reach)
        for e in entities_to_check:
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

    def get_all_entities_in_5m(self, entity):
        return [e.ei for e in self.entities if entity.position.get_dist(e.position) <= 5]

    def pos_avg(self, all_5m_ppl):
        """
        List of all ei_dir in Position form
        :param all_5m_ppl:
        :return:
        """
        x = sum([ei.x for ei in all_5m_ppl]) / len(all_5m_ppl)
        y = sum([ei.y for ei in all_5m_ppl]) / len(all_5m_ppl)

        return Position(x,y)