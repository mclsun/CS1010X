

import random
import copy
import json
import uuid
from collections import OrderedDict

######################
# Class: NamedObject #
######################

class NamedObject(object):
    def __init__(self, name):
        self.name = name
        self._id = uuid.uuid4()

    def get_name(self):
        return self.name

    def get_id(self):
        return self._id

    def json_output(self, *args, **kargs):
        return {'type': self.__class__.__name__,
                'name': self.name}

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

    def json_output(self, flat=False, *args, **kargs):
        output = super().json_output(*args, **kargs)
        if flat:
            return output

        output['objects'] = list(map(lambda obj: obj.json_output(), self.objects))
        output['neighbors'] = {k: v.json_output(flat=True) for k, v in self.neighbor_dict.items()}
        return output


#######################
# Class: MobileObject #
#######################

class MobileObject(NamedObject):
    def __init__(self, name, place):
        super().__init__(name)
        self.place = place

    def get_place(self):
        return self.place

    def json_output(self, *args, **kargs):
        output = super().json_output(*args, **kargs)
        if self.place:
            output['place'] = self.place.json_output(flat = True)
        else:
            output['place'] = None
        return output

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

    def json_output(self, *args, **kargs):
        output = super().json_output(*args, **kargs)
        if self.owner:
            output['owner'] = self.owner.json_output(flat = True)
        else:
            output['owner'] = None

        return output

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

    def json_output(self, *args, **kargs):
        output = super().json_output(*args, **kargs)
        output['health'] = self.health
        output['threshold'] = self.threshold
        return output


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

    def json_output(self, flat=False, *args, **kargs):
        output = super().json_output(*args, **kargs)
        if flat:
            return output

        output['inventory'] = list(map(lambda item: item.json_output(), self.inventory))
        return output

#######################################
# Mission 14/15
#######################################

class Weapon(Thing):
    def __init__(self, name, min_dmg, max_dmg):
        super().__init__(name)
        self.min = min_dmg
        self.max = max_dmg

    def min_damage(self):
        return self.min

    def max_damage(self):
        return self.max

    def damage(self):
        return random.randint(self.min, self.max)

    def json_output(self, *args, **kargs):
        output = super().json_output(*args, **kargs)
        output['max_dmg'] = self.max
        output['min_dmg'] = self.min
        return output

class Ammo(Thing):
    def __init__(self, name, weapon, qty):
        super().__init__(name)
        self.weapon = weapon.get_name()
        self.qty = qty

    def get_quantity(self):
        return self.qty

    def weapon_type(self):
        return self.weapon

    def remove_all(self):
        self.qty = 0

    def json_output(self, *args, **kargs):
        output = super().json_output(*args, **kargs)
        output['weapon'] = self.weapon
        output['quantity'] = self.qty
        return output

class RangedWeapon(Weapon):
    def __init__(self, name, min_dmg, max_dmg):
        super().__init__(name, min_dmg, max_dmg)
        self.shots = 0

    def shots_left(self):
        return self.shots

    def load(self, ammo):
        if ammo.weapon_type() == self.get_name():
            self.shots += ammo.get_quantity()
            ammo.remove_all()
            return True
        return False

    def damage(self):
        if self.shots_left() > 0:
            self.shots -= 1
            return super().damage()
        return 0

    def json_output(self, *args, **kargs):
        output = super().json_output(*args, **kargs)
        output['shots_left'] = self.shots
        return output

class Food(Thing):
    def __init__(self, name, food_value):
        super().__init__(name)
        self.food_value = food_value

    def get_food_value(self):
        return self.food_value

    def json_output(self, *args, **kargs):
        output = super().json_output(*args, **kargs)
        output['food_value'] = self.food_value
        return output

class Medicine(Food):
    def __init__(self, name, food_value, medicine_value):
        super().__init__(name, food_value)
        self.medicine_value = medicine_value

    def get_medicine_value(self):
        return self.medicine_value

    def json_output(self, *args, **kargs):
        output = super().json_output(*args, **kargs)
        output['medicine_value'] = self.medicine_value
        return output

class Animal(LivingThing):
    def __init__(self, name, health, food_value, *threshold):
        if threshold:
            super().__init__(name, health, threshold[0])
        else:
            super().__init__(name, health, random.randint(0,4))
        self.food_value = food_value

    def get_food_value(self):
        return self.food_value

    def go_to_heaven(self):
        food = Food(self.name + " meat", self.food_value)
        self.place.add_object(food)
        super().go_to_heaven()

    def json_output(self, *args, **kargs):
        output = super().json_output(*args, **kargs)
        output['food_value'] = self.food_value
        return output

class WildAnimal(Animal):
    def __init__(self, name, health, food_value, damage, *threshold):
        if threshold:
            super().__init__(name, health, food_value, threshold)
        else:
            super().__init__(name, health, food_value)

        self.damage = damage

        # Probability that they will attack is between 20-40%
        self.attack_probability = (random.randint(20,40)) / 100

    def attack(self, target):
        GAME_LOGGER.add_event("ATTACK", self, target, self.damage)
        target.reduce_health(self.damage)

        if target.get_health() == 0:
            GAME_LOGGER.add_event("KILLED", self, target)

    def act(self):
        targets = self.get_place().get_objects()
        targets = list(filter(lambda x: isinstance(x,Person), targets))

        attack_threshold = self.attack_probability * 100

        if targets and random.randint(0, 100) <= attack_threshold:
            target = random.choice(targets)
            self.attack(target)
        else:
            super().act()

    def get_damage(self):
        return self.damage

    def get_attack_probability(self):
        return self.attack_probability

    def json_output(self, *args, **kargs):
        output = super().json_output(*args, **kargs)
        output['damage'] = self.damage
        output['attack_probability'] = self.attack_probability
        return output

class Tribute(Person):
    def __init__(self, name, health):
        super().__init__(name, health, -1)
        self.hunger = 0

    def __eq__(self, other):
        return type(self) == type(other) and self.get_name() == other.get_name()

    def __hash__(self):
        return hash((type(self), self.get_name()))

    def get_hunger(self):
        return self.hunger

    def add_hunger(self, hunger):
        self.hunger = min(100, self.hunger+hunger)
        if self.hunger == 100:
            GAME_LOGGER.add_event("STARVED", self)
            self.go_to_heaven()

    def reduce_hunger(self, hunger):
        self.hunger = max(0, self.hunger-hunger)

    def eat(self, food):
        if food in self.inventory:
            GAME_LOGGER.add_event("ATE", self, food)
            if isinstance(food, Medicine):
                self.add_health(food.get_medicine_value())
            if isinstance(food, Food):
                self.reduce_hunger(food.get_food_value())
            self.inventory.remove(food)

    def get_weapons(self):
        inventory = self.get_inventory()
        return tuple(filter(lambda x: isinstance(x, Weapon), inventory))

    def get_food(self):
        inventory = self.get_inventory()
        return tuple(filter(lambda x: isinstance(x, Food), inventory))

    def get_medicine(self):
        inventory = self.get_inventory()
        return tuple(filter(lambda x: isinstance(x, Medicine), inventory))

    def attack(self, target, weapon):
        if weapon in self.get_weapons():
            if isinstance(target, LivingThing) and target.get_place() is self.get_place():
                dmg = weapon.damage()
                GAME_LOGGER.add_event("ATTACK", self, target, dmg)
                target.reduce_health(dmg)
                if target.get_health() == 0:
                    GAME_LOGGER.add_event("KILLED", self, target)


    def load(self, weapon, ammo):
        if weapon in self.get_inventory() and ammo in self.get_inventory():
            if isinstance(weapon, RangedWeapon):
                loaded = weapon.load(ammo)
                GAME_LOGGER.add_event("LOAD", self, weapon, ammo, loaded)

                if loaded:
                    self.inventory.remove(ammo)


    def json_output(self, *args, **kargs):
        output = super().json_output(*args, **kargs)
        output['hunger'] = self.hunger
        return output

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
    def __init__(self):
        self.reset()

    def add_map_state(self, map_state):
        self.map_states.append(copy.deepcopy(map_state))
        self.time += 1
        self.events[self.time] = []

    def add_event(self, event, *args):
        tup = (event, ) + copy.deepcopy(args)
        self.events[self.time].append(tup)

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
            'SURVIVED': lambda args: "{} has survived!".format(args[0].get_name()),
            'LOAD': lambda args: "{} loaded {} with {}".format(*(named_col(args[:-1]))) if args[-1] else
                "{} can't load {} with {}".format(*(named_col(args[:-1])))
        }
        if event in stringify:
            print(stringify[event](args))

    def print_events(self, events = None):
        if events is None:
            events = self.events

        for i in range(1, len(events)):
            print("Time:", i)
            for event in events[i]:
                self.print_event(event[0], *event[1:])
            print("")

    def warning(self, warning):
        print(warning)

    def reset(self):
        self.time = 0
        self.map_states = []
        self.events = {0:[]}


GAME_LOGGER = GameLogger()
