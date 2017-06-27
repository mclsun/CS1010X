from hungry_games_classes import *
from collections import OrderedDict
import random
import sys
import traceback


class GameConfig(object):
    def __init__(self):
        self.item_counts = OrderedDict()
        self.item_factory = DefaultItemFactory
        self.steps = 100
        self.periodic_events = []

    def set_item_count(self, item_class, count):
        self.item_counts[item_class] = count

    def add_periodic_event(self, *args):
        self.periodic_events.append(args)

class GameEngine(object):
    def __init__(self, game_map, config):
        self.map = game_map
        self.config = config
        self.tributes = []

        self.time = 0
        self.clock_list = []
        self.periodic_events = OrderedDict()

        self.prev_tributes = []
        self.map.add_factory_objects(self.config.item_factory, self.config.item_counts)

        # Add all the living objects to the clock list
        living_objects = filter(lambda obj: isinstance(obj, LivingThing), self.map.all_objects())
        self.add_to_clock(*living_objects)

    def add_tribute(self, tribute):
        self.tributes.append(tribute)
        self.add_object(tribute)

    def add_object(self, obj):
        self.map.add_object(obj)

        if isinstance(obj, LivingThing):
            self.add_to_clock(obj)

    def add_periodic_event(self, duration, fn, description):
        if duration in self.periodic_events.keys():
            self.periodic_events[duration].append(fn)
        else:
            self.periodic_events[duration] = [fn]

    def add_to_clock(self, *obj):
        self.clock_list.extend(list(obj))

    def remove_from_clock(self, obj):
        if obj in self.clock_list:
            self.clock_list.remove(obj)

    def tick(self):
        self.time += 1
        GAME_LOGGER.add_map_state(self.map.state())
        # Exceute all periodic events first
        for duration in self.periodic_events.keys():
            if self.time % duration == 0:
                for fn in self.periodic_events[duration]:
                    fn(self)

        for obj in self.clock_list:
            # If an object has gone to heaven, we do not
            # execute any command
            if obj.get_place() == HEAVEN:
                continue

            if isinstance(obj, Tribute):
                obj.add_hunger(1)
                if obj.get_place() == HEAVEN:
                    continue

                if issubclass(type(obj).__bases__[0], Tribute):
                    try:
                        self.ai_act(obj)
                    except Exception as e:
                        exception_stacktrace_list = traceback.format_exception(
                            *sys.exc_info()
                        )
                        # add 2 newlines before we print the indented stacktrace
                        exception_stacktrace_string = "\n\n{}".format(
                            "".join([
                                "    {}".format(s)
                                for s in exception_stacktrace_list
                            ])
                        )
                        GAME_LOGGER.add_event("INPUT_ERROR", obj,
                            exception_stacktrace_string
                        )
            else:
                obj.act()

        # now that everybody has acted, remove objects that are already dead from the
        # clocklist
        dead_objects = filter(lambda obj: obj.get_place() == HEAVEN, self.clock_list)
        for dead_object in dead_objects:
            self.remove_from_clock(dead_object)

        # shuffle the clocklist
        random.shuffle(self.clock_list)

    def ai_act(self, ai):
        allowed_actions = ["attack","take","eat","go","load"]
        action = ai.next_action()
        GAME_LOGGER.add_event("INPUT", ai, action)

        if action:
            verb = action[0].lower()
            if verb in allowed_actions:
                getattr(ai, verb)(*action[1:])
            else:
                GAME_LOGGER.add_event("INVALID_INPUT", ai, action)



class GameMap(object):
    def __init__(self, size, wrap=False):
        self.map = []
        self.wrap = 1 if wrap else 0
        self.size = size

        self.draw_map()

    def draw_map(self):
        # Initialize the map
        for i in range(1, self.size+1):
            self.map.append([])
            for j in range(1, self.size+1):
                place = Place(str((i,j)))
                self.map[i-1].append(place)

        # Connect the places together
        for i in range(self.size):
            for j in range(self.size-1+self.wrap):
                self.map[i][j].add_neighbor(self.map[i][(j+1)%self.size], "EAST")

        for i in range(self.size-1+self.wrap):
            for j in range(self.size):
                self.map[i][j].add_neighbor(self.map[(i+1)%self.size][j], "SOUTH")

    def add_factory_objects(self, item_factory, item_counts):
        for key in item_counts:
            for i in range(item_counts[key]):
                items = item_factory.create(key)
                for item in items:
                    self.add_object(item)

    def add_object(self, obj):
        i = random.randint(0, self.size-1)
        j = random.randint(0, self.size-1)

        self.map[i][j].add_object(obj)

    def all_objects(self):
        all_objects = []
        for i in range(self.size):
            for j in range(self.size):
                all_objects.extend(self.map[i][j].get_objects())
        return all_objects

    def state(self):
        return self.map

class ItemFactoryBuilder(object):
    def __init__(self):
        self.blueprints = OrderedDict()
        self.ranged_blueprints = OrderedDict()

    def add_ranged_weapon(self, wpn_defn, ammo_defn):
        self.add_blueprint(RangedWeapon, wpn_defn)
        self.ranged_blueprints[wpn_defn] = ammo_defn

    def add_blueprint(self, bp_class, bp_definition):
        if bp_class in self.blueprints:
            self.blueprints[bp_class].append(bp_definition)
        else:
            self.blueprints[bp_class] = [bp_definition]

    # Returns a list of objects to be created
    def create(self, bp_class):
        if bp_class in self.blueprints:
            # Choose a random blueprint definition
            defn = random.choice(self.blueprints[bp_class])

            # Given a blueprint implementation, decide on a random value amongst
            # all possible values
            args = tuple(map(lambda item: random.choice(item), defn))

            created_objs = [bp_class(*args)]

            if bp_class == RangedWeapon:
                ammo_defn = self.ranged_blueprints[defn]
                ammo_args = tuple(map(lambda item: random.choice(item), ammo_defn))
                created_objs.append(Ammo(*ammo_args))

            return created_objs


###################
# Available Items #
###################
DefaultItemFactory = ItemFactoryBuilder()
DefaultItemFactory.add_blueprint(Weapon, (('Dagger',), (10,), (12,)))
DefaultItemFactory.add_blueprint(Weapon, (('Mace',), (12,), (15,)))
DefaultItemFactory.add_blueprint(Weapon, (('Axe',), (15,), (20,)))
DefaultItemFactory.add_blueprint(Weapon, (('Sword',), (10,), (25,)))
DefaultItemFactory.add_blueprint(Weapon, (('Machete',), (15,), (25,)))

DefaultItemFactory.add_ranged_weapon((('Bow',), (20,), (25,)), (('Arrows',), (RangedWeapon('Bow', 0, 0),), range(1,2)))
DefaultItemFactory.add_ranged_weapon((('Crossbow',), (25,), (30,)), (('Bolts',), (RangedWeapon('Crossbow', 0, 0),), range(1,2)))
DefaultItemFactory.add_ranged_weapon((('Pistol',), (30,), (40,)), (('9mm',), (RangedWeapon('Pistol', 0, 0),), range(1,2)))
DefaultItemFactory.add_ranged_weapon((('Rifle',), (35,), (45,)), (('5.56mm',), (RangedWeapon('Rifle', 0, 0),), range(1,2)))

DefaultItemFactory.add_blueprint(Food, (('Carrot',), range(3,5)))
DefaultItemFactory.add_blueprint(Food, (('Potato',), range(3,5)))
DefaultItemFactory.add_blueprint(Food, (('Cabbage',), range(3,5)))
DefaultItemFactory.add_blueprint(Food, (('Apple',), range(3,5)))
DefaultItemFactory.add_blueprint(Food, (('Watermelon',), range(3,5)))

DefaultItemFactory.add_blueprint(Medicine, (('Panadol',), range(1,2), range(1,5)))
DefaultItemFactory.add_blueprint(Medicine, (('Aloe Vera',), range(1,2), range(1,5)))
DefaultItemFactory.add_blueprint(Medicine, (('Healing Herbs',), (0,), (3,)))
DefaultItemFactory.add_blueprint(Medicine, (('Health Potion',), (0,), (5,)))
DefaultItemFactory.add_blueprint(Medicine, (('Wild Mushroom',), (-1,), range(3,4)))

DefaultItemFactory.add_blueprint(Animal, (('Chicken',), range(1,5), range(5,7)))
DefaultItemFactory.add_blueprint(Animal, (('Sheep',), range(5,10), range(7,10)))
DefaultItemFactory.add_blueprint(Animal, (('Deer',), range(15,20), range(6,9)))
DefaultItemFactory.add_blueprint(Animal, (('Pig',), range(15,20), range(10,12)))
DefaultItemFactory.add_blueprint(Animal, (('Cow',), range(20,25), range(15,18)))

DefaultItemFactory.add_blueprint(WildAnimal, (('Python',), range(15,20), range(5,6), range(1,10)))
DefaultItemFactory.add_blueprint(WildAnimal, (('Boar',), range(20,25), range(10,12), range(5,10)))
DefaultItemFactory.add_blueprint(WildAnimal, (('Wolf',), range(25,30), range(6,9), range(10, 14)))
DefaultItemFactory.add_blueprint(WildAnimal, (('Bear',), range(30,35), range(15,18), range(15, 20)))
DefaultItemFactory.add_blueprint(WildAnimal, (('Mutation',), (38,), (-5,), range(20, 25)))
