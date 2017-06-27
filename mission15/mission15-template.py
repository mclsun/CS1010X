#
# CS1010X --- Programming Methodology
#
# Mission 15 Template
#
# Note that written answers are commented out to allow us to run your
# code easily while grading your problem set.

from hungry_games_classes import *
from engine import *
import simulation
import random

## remove currentplace
#change get_living things and get_things to use get_things()

# Rename XX_AI to YourName_AI
class GAB_AI(Tribute):
    def __init__(self, name, health):
        super().__init__(name, health)
        self.origin_direction = None
        self.weapon = None
        self.ammo = None
        self.loaded = False
        
    def get_living_things(self):
        return tuple([x for x in self.objects_around() if isinstance(x, LivingThing)])

    def get_things(self):
        return tuple([x for x in self.objects_around() if isinstance(x, Thing)])

    def get_ammo(self):
        return tuple([x for x in self.get_things() if isinstance(x, Ammo)])
    
    def take_things(self, things):
        for thing in things:
            return ("TAKE", thing)
        
    def choose_weapon(self, weapons, ammo):
        non_ranged_weapons = [x for x in weapons if isinstance(x, Weapon) and not isinstance(x, RangedWeapon)]
        if ammo:
            for a in ammo:
                weapon_types = {x.get_name(): x for x in weapons}
                a_weapon_type = a.weapon_type()
                if a_weapon_type in weapon_types:
                    ranged_weapon = weapon_types[a_weapon_type]
                    self.weapon = ranged_weapon
                    self.ammo = a
                    return None
        elif non_ranged_weapons:
            sorted_weapons = sorted(non_ranged_weapons, key=lambda x: x.max_damage(), reverse=True)
            self.weapon = sorted_weapons[0]
            return None
        else: #ranged weapon without ammo
            return None #self.weapon == None

    def attack_living_things(self, living_things, weapon):
        for target in living_things:
            if target.get_health() > 0:
                return ("ATTACK", target, weapon)

    def eat_food(self, food):
        for item in food:
            return ("EAT", item)

    def go_to_exit(self, exits):
        for direction in exits:
            if direction != self.origin_direction:
                self.origin_direction = opposite_direction(direction)
                return ("GO", direction)

    def load_weapon(self, weapon, ammo):
        self.loaded = True
        return ("LOAD", weapon, ammo)
        
    def next_action(self):
        '''
        if there are objects, take them
        elif there are living things and weapons
            # choose weapon (weapon or load rangedWeapon + ammo)
            # kill living things
        elif food, eat food/medicine
        elif exits (ie no things/living things) go to more places
        '''
        
        things = self.get_things()
        living_things = self.get_living_things()
        weapons = self.get_weapons()
        ammo = self.get_ammo()
        food = self.get_food()
        exits = self.get_exits()
        self.choose_weapon(weapons, ammo)

        if self.loaded == False and isinstance(self.weapon, RangedWeapon):
            return self.load_weapon(self.weapon, self.ammo)
        if living_things and self.weapon:
            return self.attack_living_things(living_things, self.weapon)
        if food:
            return self.eat_food(food)
        if things:
            return self.take_things(things)
        elif exits:
            return self.go_to_exit(exits)
        else:
            return None

# NOTE: DO NOT remove the 2 lines of code below.
#
# In particular, you will need to modify the `your_AI = XX_AI` line so that
# `XX_AI` is the name of your AI class.
# For instance, if your AI class is called `MyPrecious_AI`, then you have to
# modify that line to:
#
#     your_AI = MyPrecious_AI
#
# Failure to do so will result in the following exception on Coursemology when
# you run the test cases:
#
#     Traceback (most recent call last):
#       in <module>
#     NameError: name 'your_AI' is not defined
#
# You have been warned!
time_limit = 50 # Modify if your AI needs more than 50 moves for task 2
your_AI = GAB_AI # Modify if you changed the name of the AI class



##################
# Simulation Code
##################
##########
# Task 1 #
##########
# Goal:
# 1. Your AI should be able to pick up a Weapon / RangedWeapon
# 2. Your AI should be able to kill chicken
# 3. Your AI should be able to pick up chicken_meat after killing chicken

# Replace XX_AI with the class name of your AI
# Replace gui=True with gui=False if you do not wish to see the GUI
#simulation.task1(GAB_AI("GAB AI", 100), gui=True)


##########
# Task 2 #
##########
## 1. Your AI should be able to pick up a Weapon / RangedWeapon
## 2. Your AI should be able to move around and explore
## 3. Your AI should be able to find harmless Tribute and kill him

# Replace XX_AI with the class name of your AI
# Replace gui=True with gui=False if you do not wish to see the GUI

time_limit = 20    # You may change the time limit if your AI is taking too long
#simulation.task2(GAB_AI("GAB AI", 100), time_limit, gui=True)



#################
# Optional Task
#################
## You can create your own map and see how your AI behaves!

# Define the parameters of the map
def config():
    ## The game should have a 3x3 map
    game_map = GameMap(3)

    ## You can change the numbers to create different kinds of maps for
    ## the optional task.
    game_config = GameConfig()
    game_config.set_item_count(Weapon, 3)
    game_config.set_item_count(Animal, 10)
    game_config.set_item_count(RangedWeapon, 5)
    game_config.set_item_count(Food, 5)
    game_config.set_item_count(Medicine, 5)

    game = GameEngine(game_map, game_config)

    # Add some dummy tributes
    ryan = Tribute("Ryan", 100)
    waihon = Tribute("Wai Hon", 100)
    soedar = Tribute("Soedar", 100)

    game.add_tribute(ryan)
    game.add_tribute(waihon)
    game.add_tribute(soedar)

    # Yes, your AI can fight with himself
    #ai_clone = XX_AI("AI Clone", 100)
    #game.add_tribute(ai_clone)

    return game

# Replace XX_AI with the class name of your AI
# Replace gui=True with gui=False if you do not wish to see the GUI
simulation.optional_task(GAB_AI("GAB AI", 100), config, gui=True)
