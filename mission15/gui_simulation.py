import re
import animation
import hungry_games_classes as hgc
import cocos
import random

##################
# Grid
##################

class Grid(cocos.sprite.Sprite):
    MAX_OBJECT = 16

    def __init__(self, row, col):
        super(Grid, self).__init__("resources/grid.png")
        self.coordinate = (row, col)
        self.game_sprites = []
        for i in range(Grid.MAX_OBJECT):
            self.game_sprites.append(None)

    def get_coordinate(self):
        return self.coordinate

    def add_game_sprite(self, sprite):
        self.game_sprites[self.get_index_for_next_game_sprite()] = sprite

    def remove_game_sprite(self, sprite):
        if sprite in self.game_sprites:
            self.game_sprites[self.game_sprites.index(sprite)] = None

    def replace_game_sprite(self, new_sprite, old_sprite):
        if old_sprite in self.game_sprites:
            self.game_sprites[self.game_sprites.index(old_sprite)] = new_sprite

    def get_index_for_next_game_sprite(self):
        for i in range(len(self.game_sprites)):
            if self.game_sprites[i] is None:
                return i
        # FIXME: should handle corner case here
        return -1

    def reposition_all_game_sprites(self):
        for i in range(len(self.game_sprites)):
            sprite = self.game_sprites[i]
            if sprite is not None:
                sprite.position = self.get_position_for_game_sprite_at_index(i)

    def get_position_for_game_sprite_at_index(self, index):
        GRID_MAP = [
            [4, 8, 9, 2],
            [10, 0, 6, 11],
            [12, 7, 1, 13],
            [3, 14, 15, 5]
        ]
        for i in range(len(GRID_MAP)):
            for j in range(len(GRID_MAP[i])):
                if GRID_MAP[i][j] == index:
                    subRow = i
                    subCol = j
        subColWidth = self.width/len(GRID_MAP)
        subRowHeight = self.height/len(GRID_MAP[0])

        x = self.x - self.width/2
        y = self.y - self.height/2

        return x + (subCol + 0.5) * subColWidth, y + (subRow + 0.5) * subRowHeight

    def search_for_game_sprite(self, game_object):
        for sprite in self.game_sprites:
            if sprite is not None and sprite.get_id() == game_object.get_id():
                return sprite

        # No matching id found, try matching name instead
        for sprite in self.game_sprites:
            if sprite is not None and sprite.get_game_object().get_name() == game_object.get_name() and sprite.get_game_object().get_id() == -1:
                return sprite

        return None

    def get_next_sprite_position(self):
        return self.get_position_for_game_sprite_at_index(self.get_index_for_next_game_sprite())


##################
# GameSprite
##################

class GameSprite(cocos.sprite.Sprite):
    tribute_id = 1

    def __init__(self, game_object):
        super(GameSprite, self).__init__("resources/" + GameSprite.get_sprite_name(game_object))
        self.game_object = game_object
        self.hp_bar_sprite = None

        if isinstance(self.game_object, hgc.LivingThing):
            self.show_hp_bar()

    def get_id(self):
        return self.game_object.get_id()

    def get_game_object(self):
        return self.game_object

    @staticmethod
    def get_sprite_name(game_object):
        if isinstance(game_object, hgc.Food) and "meat" in game_object.get_name():
            return "meat.png"
        elif isinstance(game_object, hgc.Tribute):
            sprite_name = "ai" + str(GameSprite.tribute_id) + ".png"
            GameSprite.tribute_id += 1
            return sprite_name
        return game_object.get_name().lower().replace(' ', '_') + ".png"

    def show_hp_bar(self):
        self.hp_bar_sprite = cocos.sprite.Sprite("resources/hp_bar_fill.png")
        self.hp_bar_sprite.position = -self.width/2, self.height/2
        self.hp_bar_sprite.scale_x = max(0.05, self.game_object.get_health() / 100) # must show some (minimum) hp
        self.add(self.hp_bar_sprite)


##################
# GameReplayLayer
##################

class GameReplayLayer(cocos.layer.Layer):
    def __init__(self, map_size):
        super(GameReplayLayer, self).__init__()
        self.grids = []
        self.map_states = None
        self.game_events = None
        self.turn_id = None
        self.event_id = None
        self.replay_finish_callback = None

        self.create_grids(map_size)

    def create_grids(self, map_size):
        for i in range(map_size):
            row = []
            for j in range(map_size):
                grid = Grid(i, j)
                grid.position = (j + 0.5) * grid.width, (i + 0.5) * grid.height
                self.add(grid)
                row.append(grid)
            self.grids.append(row)

    def replay(self, game_events, map_states, callback=None, start_turn=0, start_event=0):
        self.game_events = game_events
        self.map_states = map_states
        self.replay_finish_callback = callback
        self.turn_id = start_turn - 1  # increase back in replay_next_turn
        self.replay_next_turn(start_event)

    def replay_next_turn(self, start_event=0):
        self.turn_id += 1
        if self.turn_id >= len(self.game_events):
            if self.replay_finish_callback:
                self.replay_finish_callback()
            return

        print("Time " + str(self.turn_id + 1) + ":")
        self.load_new_game_objects()
        self.event_id = start_event - 1  # increase back in replay_next_event
        self.replay_next_event()

    def load_new_game_objects(self):
        map_state = self.map_states[self.turn_id]
        for row in map_state:
            for place in row:
                grid = self.get_grid_from_place(place)
                for game_object in place.get_objects():
                    if grid.search_for_game_sprite(game_object) is None:
                        self.load_game_object(game_object, grid)
        self.reposition_all_game_objects()

    def load_game_object(self, game_object, grid):
        sprite = GameSprite(game_object)
        self.add(sprite)
        grid.add_game_sprite(sprite)

    def reposition_all_game_objects(self):
        for row in self.grids:
            for grid in row:
                grid.reposition_all_game_sprites()

    def replay_next_event(self):
        self.event_id += 1
        if self.event_id >= len(self.game_events[self.turn_id]):
            print()
            self.replay_next_turn()
            return

        event = self.game_events[self.turn_id][self.event_id]

        hgc.GAME_LOGGER.print_event(event[0], *event[1:])

        if GameReplayLayer.should_replay_event(event):
            self.replay_event(event)
        else:
            self.replay_next_event()

    @staticmethod
    def should_replay_event(event):
        return event[0] in ['MOVE', 'ATTACK', 'TOOK', 'KILLED', 'SPAWNED', 'ATE']

    def replay_event(self, event):
        handlers = {
            'MOVE': self.replay_move_event,
            'TOOK': self.replay_take_event,
            'ATTACK': self.replay_attack_event,
            'KILLED': self.replay_dead_event,
            'SPAWNED': self.replay_spawn_event,
            'ATE' : self.replay_eat_event
        }

        if event[0] in handlers:
            handlers[event[0]](event)
        else:
            print("Unknown event: " + event[0])

    def replay_move_event(self, event):
        from_grid = self.get_grid_from_place(event[2])
        sprite = from_grid.search_for_game_sprite(event[1])
        to_grid = self.get_grid_from_place(event[3])

        self.animate_move_event(sprite, to_grid)
        from_grid.remove_game_sprite(sprite)
        to_grid.add_game_sprite(sprite)

    def get_grid_from_place(self, place):
        place_name = place.get_name()
        tokens = re.sub("[(),]", "", place_name).split(" ")
        row = int(tokens[0]) - 1
        col = int(tokens[1]) - 1
        return self.grids[row][col]

    def animate_move_event(self, sprite, to_grid):
        animation.animate_move(sprite, to_grid, self.replay_next_event)

    def replay_take_event(self, event):
        grid = self.get_grid_from_place(event[1].get_place())
        taking_sprite = grid.search_for_game_sprite(event[1])
        taken_sprite = grid.search_for_game_sprite(event[2])

        self.animate_take_event(taking_sprite, taken_sprite, grid)

    def animate_take_event(self, taking_sprite, taken_sprite, grid):
        animation.animate_take(taking_sprite, taken_sprite, grid, self.handle_take_animation_end)

    def handle_take_animation_end(self, taken_sprite, grid):
        grid.remove_game_sprite(taken_sprite)
        self.remove(taken_sprite)
        self.replay_next_event()

    def replay_attack_event(self, event):
        attacking_grid = self.get_grid_from_place(event[1].get_place())
        attacking_sprite = attacking_grid.search_for_game_sprite(event[1])
        attacked_grid = self.get_grid_from_place(event[2].get_place())
        attacked_sprite = attacked_grid.search_for_game_sprite(event[2])
        new_hp = max(0, event[2].get_health() - event[3])

        self.animate_attack_event(attacking_sprite, attacked_sprite, new_hp)

    def animate_attack_event(self, attacking_sprite, attacked_sprite, new_hp):
        animation.animate_attack(attacking_sprite, attacked_sprite, new_hp, self.replay_next_event)

    def replay_dead_event(self, event):
        grid = self.get_grid_from_place(event[1].get_place())
        dead_sprite = grid.search_for_game_sprite(event[2])
        self.animate_dead_event(dead_sprite, grid)

    def animate_dead_event(self, dead_sprite, grid):
        animation.animate_dead(dead_sprite, grid, self.handle_dead_animation_end)

    def handle_dead_animation_end(self, dead_sprite, grid):
        if isinstance(dead_sprite.get_game_object(), hgc.Animal):
            if self.turn_id + 1 < len(self.game_events):
                self.forward_load_animal_meat(self.map_states[self.turn_id + 1], dead_sprite, grid)
        else:
            self.remove(dead_sprite)
            grid.remove_game_sprite(dead_sprite)
        self.replay_next_event()

    def forward_load_animal_meat(self, map_state, dead_sprite, grid):
        row, col = grid.get_coordinate()
        place = map_state[row][col]
        find_meat = False
        for game_object in place.get_objects():
            if isinstance(game_object, hgc.Food) and dead_sprite.get_game_object().get_name() in game_object.get_name() and "meat" in game_object.get_name():
                meat = game_object
                find_meat = True
                break

        if not find_meat: # meat is spawned and taken in the same turn
            dead_object = dead_sprite.get_game_object();
            meat = hgc.Food(dead_object.get_name() + " meat", dead_object.get_food_value())
            # hack to invalidate meat
            meat._id = -1
        
        meat_sprite = GameSprite(meat)
        meat_sprite.position = dead_sprite.position

        grid.replace_game_sprite(meat_sprite, dead_sprite)
        self.remove(dead_sprite)
        self.add(meat_sprite)

    def replay_spawn_event(self, event):
        grid = self.get_grid_from_place(event[1].get_place())
        sprite = GameSprite(event[1])

        sprite.position = grid.get_next_sprite_position()
        self.add(sprite)
        grid.add_game_sprite(sprite)

        self.animate_spawn_event(sprite)

    def animate_spawn_event(self, spawned_sprite):
        animation.animate_spawn(spawned_sprite, self.replay_next_event)

    def replay_eat_event(self, event):
        grid = self.get_grid_from_place(event[1].get_place())
        sprite = grid.search_for_game_sprite(event[1])
        new_hp = min(100, event[1].get_health() + event[2].get_food_value())
        self.animate_eat_event(sprite, new_hp)

    def animate_eat_event(self, sprite, new_hp):
        animation.animate_eat(sprite, new_hp, self.replay_next_event)

##################
# Misc Functions #
##################

def animate_game_logger_events(grid_size, callback=None):
    animate_game_events(grid_size, hgc.GAME_LOGGER.events, hgc.GAME_LOGGER.map_states, callback)

def animate_game_events(grid_size, game_events, map_states, callback=None):
    # print("\n\n-----GUI Simulation-----")
    grid_width, grid_heigh = 128, 128
    cocos.director.director.init(width=grid_size * grid_width, height=grid_size * grid_heigh)
    game_replay_layer = GameReplayLayer(grid_size)
    main_scene = cocos.scene.Scene(game_replay_layer)
    converted_game_events = []
    for i in range(1, len(game_events)):
        converted_game_events.append(game_events[i])
    
    game_replay_layer.replay(converted_game_events, map_states, callback)
    cocos.director.director.run(main_scene)