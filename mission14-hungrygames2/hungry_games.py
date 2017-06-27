import random
from collections import OrderedDict

######################
# Class: NamedObject #
######################

class NamedObject(object):
    def __init__(self, name):
        self.name = name

    def get_name(self):
        return self.name

################
# Class: Place #
################

class Place(NamedObject):
    def __init__(self, name):
        super().__init__(name)
        self.objects = []

        # maps direction -> place
        self.neighbor_dict = OrderedDict()

    def add_object(self, new_object):
        if isinstance(new_object, Thing) or isinstance(new_object, LivingThing):
            self.objects.append(new_object)
            new_object.place = self
        else:
            GAME_LOGGER.warning("You can only add Thing or LivingThing to {}".format(self.get_name()))

    def del_object(self, curr_object):
        if curr_object in self.objects:
            self.objects.remove(curr_object)
            curr_object.place = None
        else:
            GAME_LOGGER.warning("Cannot remove object, as it is not in {}".format(self.get_name()))

    def get_objects(self):
        return self.objects

    def get_exits(self):
        return list(self.neighbor_dict.keys())

    def add_neighbor(self, new_neighbor, direction):
        if isinstance(new_neighbor, Place):
            opp_dir = opposite_direction(direction)
            # We have to ensure that we can add the neighbor to the current place
            if direction not in self.neighbor_dict.keys() and opp_dir not in new_neighbor.neighbor_dict.keys():
                self.neighbor_dict[direction] = new_neighbor
                new_neighbor.neighbor_dict[opp_dir] = self
            else:
                GAME_LOGGER.warning("A neighbor has already been assigned")
        else:
            GAME_LOGGER.warning("{} should be of type Place".format(new_neighbor.get_name()))

    def get_neighbors(self):
        return list(self.neighbor_dict.values())

    def get_neighbor_at(self, direction):
        return self.neighbor_dict.get(direction, None)

    def random_neighbor(self):
        neighbors = self.get_neighbors()
        if neighbors:
            return random.choice(self.get_neighbors())
        return None

#######################
# Class: MobileObject #
#######################

class MobileObject(NamedObject):
    def __init__(self, name, place):
        super().__init__(name)
        self.place = place

    def get_place(self):
        return self.place

################
# Class: Thing #
################

class Thing(MobileObject):
    def __init__(self, name):
        super().__init__(name, None)
        self.owner = None

    def set_owner(self, owner):
        self.owner = owner

    def get_owner(self):
        return self.owner

    def is_owned(self):
        return self.owner is not None

######################
# Class: LivingThing #
######################

class LivingThing(MobileObject):
    def __init__(self, name, health, threshold):
        super().__init__(name, None)
        self.health = health
        self.threshold = threshold

    def get_threshold(self):
        return self.threshold

    def get_health(self):
        return self.health

    def add_health(self, health):
        self.health = min(100, self.health+health)

    def reduce_health(self, health):
        self.health = max(0, self.health-health)
        if self.health == 0:
            self.go_to_heaven()

    def go_to_heaven(self):
        self.get_place().del_object(self)
        HEAVEN.add_object(self)
        GAME_LOGGER.add_event("DEAD", self)

    def move_to(self, new_place):
        old_place = self.get_place()

        # we can only move to one of the neighboring place
        if new_place in old_place.get_neighbors():
            GAME_LOGGER.add_event("MOVE", self, old_place, new_place)
            old_place.del_object(self)
            new_place.add_object(self)
        else:
            GAME_LOGGER.warning("{} cannot move from {} to {}".format(self.get_name(), old_place.get_name(), new_place.get_name()))

    def act(self):
        if self.threshold >= 0 and random.randint(0, self.threshold) == 0:
            new_place = self.get_place().random_neighbor()
            if new_place:
                self.move_to(new_place)


#################
# Class: Person #
#################

class Person(LivingThing):
    def __init__(self, name, health, threshold):
        self.inventory = []
        super().__init__(name, health, threshold)

    def take(self, thing):
        # Can only take things in current location and not owned by others
        if isinstance(thing, Thing) and thing in self.place.objects and not thing.is_owned():
            thing.set_owner(self)
            self.inventory.append(thing)
            self.place.del_object(thing)
            GAME_LOGGER.add_event("TOOK", self, thing)
        else:
            GAME_LOGGER.warning("{} cannot take {}.".format(self.get_name(), thing.get_name()))

    def remove_item(self, thing):
        #Can only remove things in inventory
        if isinstance(thing, Thing) and thing in self.get_inventory() and thing.get_owner()==self:
            thing.set_owner(None)
            self.inventory.remove(thing)
        else:
            GAME_LOGGER.warning("{} does not own {}.".format(self.get_name(), thing.get_name()))

    def go(self, direction):
        new_place = self.place.get_neighbor_at(direction.upper())
        if new_place is not None:
            self.move_to(new_place)
        else:
            GAME_LOGGER.warning("{} cannot go {} from {}".format(self.get_name(), direction, self.get_place().get_name()))

    def get_inventory(self):
        return list(self.inventory)

    def objects_around(self):
        return list(filter(lambda t: t is not self, self.get_place().get_objects()))

    def get_exits(self):
        return self.get_place().get_exits()


##################
# Misc Functions #
##################

# define places
BASE = Place("Base")
HEAVEN = Place("Heaven")

# define direction
up = "UP"
down = "DOWN"
north = "NORTH"
south = "SOUTH"
east = "EAST"
west = "WEST"

global_directions = ['NORTH', 'EAST', 'UP','SOUTH', 'WEST', 'DOWN']

# Helper functions
def opposite_direction(direction):
    index = ['NORTH', 'EAST', 'UP','SOUTH', 'WEST', 'DOWN'].index(direction)
    index = (index+3) % 6
    return global_directions[index]

def named_col(col):
    # Only accepts tuple/list
    type_col = type(col)
    if type_col != list and type_col != tuple:
        return None

    return type_col(map(lambda x: x.get_name() if isinstance(x, NamedObject) else x, col))

class GameLogger(object):
    def add_event(self, event, *args):
        self.print_event(event, *args)

    def print_event(self, event, *args):
        stringify = {
            'MOVE': lambda args: "{} moved from {} to {}".format(*(named_col(args))),
            'INPUT': lambda args: "{} executed {}".format(args[0].get_name(), named_col(args[1])),
            'INPUT_ERROR': lambda args: "{}'s AI raised an exception: {}".format(args[0].get_name(), args[1]),
            'TOOK': lambda args: "{} took {}".format(*(named_col(args))),
            'ATE': lambda args: "{} ate {}".format(*(named_col(args))),
            'STARVED': lambda args: "{} starved!".format(args[0].get_name()),
            'DEAD': lambda args: "{} went to heaven!".format(args[0].get_name()),
            'ATTACK': lambda args: "{} attacked {} ({} dmg)".format(args[0].get_name(),
                args[1].get_name(), args[2]),
            'KILLED': lambda args: "{} killed {}".format(args[0].get_name(), args[1].get_name()),
            'SPAWNED': lambda args: "{} is spawned!".format(args[0].get_name()),
            'SURVIVED': lambda args: "{} has survived!".format(args[0].get_name())
        }
        if event in stringify:
            print(stringify[event](args))

    def warning(self, warning):
        print(warning)

GAME_LOGGER = GameLogger()
