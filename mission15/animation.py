import cocos
import random

class Shake(cocos.actions.IntervalAction):
    def __init__(self, strength, duration):
        self.strength = strength
        self.duration = duration
        self.start_position = None

    def start(self):
        self.start_position = self.target.position

    def stop(self):
        self.target.position = self.start_position

    def update(self, t):
        rand_x = random.randrange(-self.strength, self.strength)
        rand_y = random.randrange(-self.strength, self.strength)
        x, y = self.start_position

        self.target.position = x + rand_x, y + rand_y

class ScaleXTo(cocos.actions.IntervalAction):
    def __init__(self, scale, duration):
        self.end_scale = scale
        self.duration = duration
        self.start_scale = None
        self.delta = None

    def start(self):
        self.start_scale = self.target.scale_x
        self.delta = self.end_scale-self.start_scale

    def update(self, t):
        self.target.scale_x = self.start_scale + self.delta * t


def cc_sequence(*args):
    if len(args) == 2:
        return cocos.actions.sequence(*args)
    else:
        return cocos.actions.sequence(args[0], cc_sequence(*args[1:]))


def animate_move(sprite, to_grid, callback):
    MOVE_ANIMATION_DURATION = 0.01

    move_action = cocos.actions.MoveTo(to_grid.get_next_sprite_position(), MOVE_ANIMATION_DURATION)
    end_action = cocos.actions.CallFunc(callback)
    sprite.do(cocos.actions.sequence(move_action, end_action))


def animate_take(taking_sprite, taken_sprite, grid, callback):
    TAKE_ANIMATION_DURATION = 0.01

    move_action = cocos.actions.MoveTo(taking_sprite.position, TAKE_ANIMATION_DURATION)
    fade_action = cocos.actions.FadeOut(TAKE_ANIMATION_DURATION)
    end_action = cocos.actions.CallFunc(callback, taken_sprite, grid)

    taken_sprite.do(cocos.actions.sequence(cocos.actions.spawn(move_action, fade_action), end_action))


def animate_attack(attacking_sprite, attacked_sprite, new_hp, callback):
    ATTACK_WITHDRAW_ANIMATION_DURATION = 0.01
    FLINCH_ANIMATION_DURATION = 0.02 # must be longer than 2 * withdraw dration
    UPDATE_HP_DURATION = 0.02

    def animate_update_target_hp():
        scale_x = (max(5, new_hp) if new_hp else 0) / 100 # must show some (minimum) hp
        update_hp_action = ScaleXTo(scale_x, UPDATE_HP_DURATION)
        end_action = cocos.actions.CallFunc(callback)
        attacked_sprite.hp_bar_sprite.do(cc_sequence(update_hp_action, end_action))

    def animate_target_flinch():
        shake_action = Shake(5, FLINCH_ANIMATION_DURATION)
        update_hp_action = cocos.actions.CallFunc(animate_update_target_hp)
        attacked_sprite.do(cc_sequence(shake_action, update_hp_action))

    actions = [
        cocos.actions.MoveTo(attacked_sprite.position, ATTACK_WITHDRAW_ANIMATION_DURATION),
        cocos.actions.CallFunc(animate_target_flinch),
        cocos.actions.MoveTo(attacking_sprite.position, ATTACK_WITHDRAW_ANIMATION_DURATION)
    ]

    attacking_sprite.do(cc_sequence(*actions))


def animate_dead(dead_sprite, grid, callback):
    DEAD_ANIMATION_DURATION = 0.01

    fade_action = cocos.actions.FadeOut(DEAD_ANIMATION_DURATION)
    end_action = cocos.actions.CallFunc(callback, dead_sprite, grid)
    dead_sprite.do(cocos.actions.sequence(fade_action, end_action))

def animate_spawn(spawned_sprite, callback):
    SPAWN_ANIMATION_DURATION = 0.01

    fade_action = cocos.actions.FadeIn(SPAWN_ANIMATION_DURATION)
    end_action = cocos.actions.CallFunc(callback)

    spawned_sprite.do(cocos.actions.sequence(fade_action, end_action))

def animate_eat(sprite, new_hp, callback):
    EAT_ANIMATION_DURATION = 1
    update_hp_action = ScaleXTo(new_hp/100, EAT_ANIMATION_DURATION)
    end_action = cocos.actions.CallFunc(callback)
    sprite.hp_bar_sprite.do(cc_sequence(update_hp_action, end_action))
