from hungry_games_classes import *
from engine import *
import gui_simulation

##########
# Task 1 #
##########
def task1(tribute_ai, gui=False):
    GAME_LOGGER.reset()
    chicken = Animal("Chicken", 30, 10)
    axe = Weapon("Axe",5,15)
    bow = RangedWeapon("Bow", 10, 20)
    arrow = Ammo("Arrows", bow, 5)

    game_map = GameMap(1)

    game = GameEngine(game_map, GameConfig())
    game.add_tribute(tribute_ai)
    game.add_object(chicken)
    game.add_object(axe)
    game.add_object(bow)
    game.add_object(arrow)

    has_food = 0
    print("====== Task 1 ======")
    while game.time < 20 and has_food == 0:
        game.tick()
        inventory = tribute_ai.get_inventory()
        has_food = len(list(filter(lambda x: isinstance(x, Food), inventory)))

    if not gui:
        GAME_LOGGER.print_events()
    else:
        def simulation_finish_callback():
            if has_food:
                print("You survived!")
            else:
                print("Try again?")

        gui_simulation.animate_game_logger_events(1, simulation_finish_callback)



##########
# Task 2 #
##########
def task2(tribute_ai, time_limit, gui=False):
    GAME_LOGGER.reset()
    game_map = GameMap(2)
    game_config = GameConfig()
    game_config.set_item_count(Weapon, 3)
    game = GameEngine(game_map, game_config)

    ken = Tribute("Ken", 100)

    game.add_tribute(ken)
    game.add_tribute(tribute_ai)

    print("====== Task 2 ======")
    while ken in game.clock_list and game.time < time_limit:
        game.tick()

    if not gui:
        GAME_LOGGER.print_events()
    else:
        def simulation_finish_callback():
            if ken in game.clock_list:
                print("Try again...or extend the time limit")
            else:
                print("You passed!")

        gui_simulation.animate_game_logger_events(2, simulation_finish_callback)

#################
# Optional Task #
#################
def optional_task(tribute_ai, config, gui=False):
    GAME_LOGGER.reset()
    game = config()
    game.add_tribute(tribute_ai)

    clock_list = game.clock_list

    print("====== Optional Task ======")
    while len(list(filter(lambda x: isinstance(x, Tribute), clock_list))) > 1:
        game.tick()


    if not gui:
        GAME_LOGGER.print_events()

    else:
        def simulation_finish_callback():
            winner =  list(filter(lambda x: isinstance(x, Tribute), clock_list))
            if winner:
                print("\nWinner is",winner[0].name)
            else:
                print("\nThere is no winner!")

        gui_simulation.animate_game_logger_events(game.map.size, simulation_finish_callback)
